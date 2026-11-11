#!/usr/bin/env python3
"""Central de Pessoas Kora Foods - servidor local stdlib + openpyxl. Porta 8765."""
import json, pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime, date
import openpyxl

XLSX = pathlib.Path(__file__).parent / "03 - Arquivo Apoio - Pessoas_RH.xlsx"
REF = "2026-10-15"

def _load():
    import unicodedata
    def norm(s):
        return unicodedata.normalize("NFKD", str(s)).encode("ascii","ignore").decode()
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    def sh(name):
        ws = wb[name]
        rows = list(ws.iter_rows(values_only=True))
        hdr = [norm(h) for h in rows[0]]
        return [dict(zip(hdr, r)) for r in rows[1:] if r[0] is not None]
    def conv(v):
        if isinstance(v, datetime): return v.date().isoformat()
        if isinstance(v, date): return v.isoformat()
        return v
    col = sh("Colaboradores"); mov = sh("Movimentações"); fer = sh("Férias"); des = sh("Desligamentos")
    for c in col: c["Data de admissao"] = conv(c.get("Data de admissao"))
    for m in mov: m["Data"] = conv(m["Data"])
    for f in fer:
        for k in ("Inicio do aquisitivo","Fim do aquisitivo","Limite para gozo","Inicio do gozo"):
            if f.get(k): f[k] = conv(f[k])
    for d in des: d["Data"] = conv(d["Data"])
    # cards
    ativos = [c for c in col if c["Status"]=="Ativo"]
    sal = {c["Matricula"]: float(c["Salario"] or 0) for c in col}
    ref = date.fromisoformat(REF)
    venc=[]; v60=[]
    for f in fer:
        lim = f["Limite para gozo"]
        if not lim: continue
        lm = datetime.fromisoformat(lim).date()
        dias = float(f["Dias de direito"] or 0)
        custo = sal.get(f["Matricula"],0)*dias/30
        if f["Status"]=="Pendente" and lm < ref:
            venc.append({"mat":f["Matricula"],"limite":lim,"dias":dias,"custo":custo})
        if f["Status"]!="Realizada" and ref <= lm <= date.fromordinal(ref.toordinal()+60):
            v60.append({"mat":f["Matricula"],"limite":lim,"dias":dias,"custo":custo})
    venc.sort(key=lambda x:-x["custo"]); v60.sort(key=lambda x:x["limite"])
    cards = {"ativos": len(ativos), "total": len(col),
             "ferias_vencidas_qtd": len(venc), "ferias_vencidas_custo": round(sum(x["custo"] for x in venc),2),
             "ferias_60d_qtd": len(v60), "vencidas": venc, "vencendo": v60}
    return {"ref":"15/10/2026","cards":cards,"colaboradores":col,"movimentacoes":mov,"ferias":fer,"desligamentos":des}

class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
    def _json(self, obj, code=200):
        body = json.dumps(obj, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ("/","/index.html"):
            data = (pathlib.Path(__file__).parent / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self._cors()
            self.end_headers()
            self.wfile.write(data)
        elif u.path == "/api/dados":
            try:
                self._json(_load())
            except Exception as e:
                self._json({"erro": str(e)}, 500)
        else:
            self.send_response(404); self.end_headers()
    def do_POST(self):
        ln = int(self.headers.get("Content-Length",0)); body = self.rfile.read(ln)
        try:
            data = json.loads(body or b"{}")
        except Exception:
            self._json({"ok": False, "msg": "Corpo da requisição inválido."}); return
        wb = openpyxl.load_workbook(XLSX)
        if self.path == "/api/promocao":
            mat = data.get("matricula"); cargo_n = data.get("cargo"); sal_n = data.get("salario"); dt = data.get("data") or REF
            if not mat or not cargo_n:
                self._json({"ok": False, "msg": "Preencha matrícula e cargo."}); return
            try:
                sal_num = float(sal_n)
            except (TypeError, ValueError):
                self._json({"ok": False, "msg": "Salário inválido. Informe um número (ex.: 3500)."}); return
            try:
                dt_data = datetime.fromisoformat(dt).date()
            except (TypeError, ValueError):
                self._json({"ok": False, "msg": "Data inválida. Use o formato AAAA-MM-DD."}); return
            ws = wb["Colaboradores"]
            achou = False
            for row in ws.iter_rows(min_row=2):
                if row[0].value == mat:
                    cargo_a, sal_a = row[3].value, row[6].value
                    row[3].value = cargo_n; row[6].value = sal_num
                    achou = True; break
            if not achou:
                self._json({"ok": False, "msg": "Matrícula não encontrada."}); return
            wb["Movimentações"].append([mat, dt_data, "Promoção", cargo_a, cargo_n, float(sal_a or 0), sal_num, "Registrado via Central de Pessoas"])
            wb.save(XLSX)
            self._json({"ok": True, "msg": "Promoção registrada e gravada na planilha."})
        elif self.path == "/api/ferias":
            mat = data.get("matricula"); ini = data.get("inicio")
            if not mat:
                self._json({"ok": False, "msg": "Informe a matrícula."}); return
            try:
                ini_data = datetime.fromisoformat(ini).date()
            except (TypeError, ValueError):
                self._json({"ok": False, "msg": "Data de início inválida. Use o formato AAAA-MM-DD."}); return
            ws = wb["Férias"]
            achou = False
            for row in ws.iter_rows(min_row=2):
                if row[0].value == mat and row[7].value == "Pendente":
                    row[6].value = ini_data; row[7].value = "Programada"; achou = True; break
            if not achou:
                self._json({"ok": False, "msg": "Nenhuma férias pendente encontrada."}); return
            wb.save(XLSX)
            self._json({"ok": True, "msg": "Férias programadas e gravadas na planilha."})
        else:
            self.send_response(404); self.end_headers()
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header("Content-Length","0")
        self.end_headers()
    def log_message(self,*a): pass

if __name__=="__main__":
    print("Central rodando em http://192.168.15.17:8765")
    HTTPServer(("192.168.15.17",8765), H).serve_forever()
