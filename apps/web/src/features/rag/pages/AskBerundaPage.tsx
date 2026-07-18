import { useState } from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useMutation } from "@/hooks/useApi";
import { Send, Bot, User, AlertCircle } from "lucide-react";
import type { RAGResponse, RAGQuery } from "@/types/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: RAGResponse["citations"];
}

export default function AskBerundaPage() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello! I am Berunda AI. Ask me anything about the crime cases in natural language.",
    },
  ]);
  const { isLoading, mutate } = useMutation<RAGResponse>("/rag/query");

  const handleSubmit = async () => {
    if (!query.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: query };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");

    const body: RAGQuery = { query };
    const response = await mutate(body);

    if (response) {
      const assistantMessage: Message = {
        role: "assistant",
        content: response.answer,
        citations: response.citations,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } else {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I'm sorry, I could not process your query. Please try again.",
        },
      ]);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Ask Berunda</h1>
        <p className="mt-1 text-sm text-surface-400">
          Natural language query interface for crime data
        </p>
      </div>

      <Card className="flex h-[600px] flex-col">
        <div className="flex-1 space-y-4 overflow-y-auto">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex gap-3 ${msg.role === "user" ? "justify-end" : ""}`}
            >
              {msg.role === "assistant" && (
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-berunda-600">
                  <Bot size={16} className="text-white" />
                </div>
              )}
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  msg.role === "user"
                    ? "bg-berunda-600 text-white"
                    : "bg-surface-700 text-surface-200"
                }`}
              >
                <p className="text-sm">{msg.content}</p>
                {msg.citations && msg.citations.length > 0 && (
                  <div className="mt-2 border-t border-surface-600 pt-2">
                    <p className="mb-1 text-xs font-medium text-surface-400">
                      Sources:
                    </p>
                    {msg.citations.map((c, j) => (
                      <p key={j} className="text-xs text-surface-400">
                        {c.caseNumber} (relevance: {(c.relevance * 100).toFixed(0)}%)
                      </p>
                    ))}
                  </div>
                )}
              </div>
              {msg.role === "user" && (
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface-600">
                  <User size={16} className="text-white" />
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="flex gap-3">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-berunda-600">
                <Bot size={16} className="text-white" />
              </div>
              <div className="rounded-lg bg-surface-700 px-4 py-2">
                <LoadingSpinner size="sm" />
              </div>
            </div>
          )}
        </div>

        <div className="mt-4 flex gap-2 border-t border-surface-700 pt-4">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            placeholder="Ask a question about crime data..."
            className="flex-1"
          />
          <Button onClick={handleSubmit} isLoading={isLoading}>
            <Send size={16} />
          </Button>
        </div>
      </Card>
    </div>
  );
}
