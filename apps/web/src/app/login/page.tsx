import { Button } from "@/components/ui/button";
import { messages } from "@/i18n";

export default function LoginPage() {
  return (
    <main className="flex min-h-dvh items-center justify-center p-6">
      <section aria-labelledby="login-title" className="w-full max-w-lg rounded-xl border border-border bg-white p-8 shadow-sm">
        <p className="mb-8 text-sm font-medium text-primary">{messages.app.name}</p>
        <p className="mb-3 text-sm">{messages.login.stage}</p>
        <h1 id="login-title" className="mb-4 text-3xl font-semibold">{messages.login.title}</h1>
        <p id="unavailable-reason" className="mb-6 leading-relaxed">{messages.login.description}</p>
        <Button disabled aria-describedby="unavailable-reason" className="w-full">{messages.login.action}</Button>
        <p className="mt-4 text-sm">{messages.login.notice}</p>
      </section>
    </main>
  );
}
