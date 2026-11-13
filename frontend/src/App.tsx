import { ArrowDownToLine, FileText, LoaderCircle, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";

const MAX_SIZE = 4 * 1024 * 1024;

export default function App() {
  const input = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [download, setDownload] = useState("");

  useEffect(
    () => () => {
      if (download) URL.revokeObjectURL(download);
    },
    [download],
  );

  function selectFile(files: FileList | null) {
    setError("");
    setFile(null);
    setDownload("");
    if (!files?.length) return;
    if (files.length !== 1) {
      setError("Envie um arquivo por vez.");
      return;
    }
    const selected = files[0];
    if (!/\.(pdf|jpe?g|txt)$/i.test(selected.name)) {
      setError("Escolha um arquivo PDF, JPG ou TXT.");
      return;
    }
    if (!selected.size || selected.size > MAX_SIZE) {
      setError("O arquivo deve ter conteúdo e no máximo 4 MB.");
      return;
    }
    setFile(selected);
  }

  async function convert() {
    if (!file || busy) return;
    setBusy(true);
    setError("");
    setDownload("");
    try {
      const body = new FormData();
      body.append("file", file);
      const response = await fetch("/api/extract", { method: "POST", body });
      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(
          typeof data?.detail === "string"
            ? data.detail
            : "Não foi possível converter o arquivo. Tente novamente.",
        );
      }
      setDownload(URL.createObjectURL(await response.blob()));
    } catch (err) {
      setError(
        err instanceof TypeError
          ? "Não foi possível conectar ao servidor. Verifique se a API está em execução."
          : err instanceof Error
            ? err.message
            : "Ocorreu um erro ao converter.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto max-w-xl px-5 py-10">
      <h1 className="text-xl font-semibold text-primary">
        Converter cardápio para Excel
      </h1>
      <p className="mt-2 text-sm text-muted-foreground">
        PDF, JPG ou TXT. Um arquivo por vez, até 4 MB.
      </p>

      <section
        className="mt-6 rounded-lg border border-border bg-card p-5"
        aria-label="Conversão de arquivo"
      >
        <label htmlFor="menu-file" className="mb-2 block text-sm font-medium">
          Arquivo do cardápio
        </label>
        <input
          id="menu-file"
          ref={input}
          type="file"
          accept=".pdf,.jpg,.jpeg,.txt"
          disabled={busy}
          className="block w-full min-w-0 rounded-md border border-border text-sm text-muted-foreground file:mr-3 file:cursor-pointer file:border-0 file:border-r file:border-border file:bg-muted file:px-3 file:py-2 file:text-sm file:font-medium file:text-primary hover:file:bg-accent focus-visible:outline-2 focus-visible:outline-primary disabled:opacity-50"
          onChange={(e) => {
            selectFile(e.target.files);
          }}
        />

        {file && (
          <div className="mt-3 flex items-center gap-2 text-sm">
            <FileText size={16} className="shrink-0 text-muted-foreground" />
            <span className="min-w-0 flex-1 truncate" title={file.name}>
              {file.name}
              <span className="ml-2 text-xs text-muted-foreground">
                {(file.size / 1024).toFixed(1)} KB
              </span>
            </span>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              disabled={busy}
              aria-label="Remover arquivo"
              onClick={() => {
                if (input.current) input.current.value = "";
                setFile(null);
                setDownload("");
                setError("");
              }}
            >
              <X />
            </Button>
          </div>
        )}

        <div className="mt-5 flex flex-wrap gap-3">
          <Button type="button" disabled={!file || busy} onClick={convert}>
            {busy && <LoaderCircle className="animate-spin" />}
            {busy ? "Convertendo..." : "Gerar XLSX"}
          </Button>
          {download && (
            <Button asChild variant="secondary">
              <a href={download} download="cardapio.xlsx">
                <ArrowDownToLine /> Baixar XLSX
              </a>
            </Button>
          )}
        </div>

        <div aria-live="polite" aria-atomic="true">
          {busy && (
            <p className="mt-3 text-sm text-muted-foreground">
              Processando arquivo. Aguarde.
            </p>
          )}
          {download && (
            <p className="mt-3 border-l-2 border-secondary pl-2 text-sm text-primary">
              Planilha gerada: cardapio.xlsx.
            </p>
          )}
          {error && (
            <p role="alert" className="mt-3 text-sm text-destructive">
              {error}
            </p>
          )}
        </div>
      </section>

      <section className="mt-6 text-sm" aria-labelledby="txt-heading">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 id="txt-heading" className="font-medium">
            Formato do TXT
          </h2>
          <a
            href="/modelo-cardapio.txt"
            download="modelo-cardapio.txt"
            className="text-primary underline underline-offset-4 hover:decoration-secondary hover:decoration-2 focus-visible:outline-2 focus-visible:outline-primary"
          >
            Baixar modelo TXT
          </a>
        </div>
        <pre className="mt-3 overflow-x-auto rounded-md border border-border bg-card p-3 font-mono text-xs leading-6">
          {"CATEGORIA\nPRODUTO R$10,00"}
        </pre>
        <p className="mt-2 text-xs leading-5 text-muted-foreground">
          Categoria em uma linha, produtos nas seguintes. Preços com vírgula e
          duas casas decimais. Salve em UTF-8.
        </p>
      </section>
    </main>
  );
}
