"use client";

import { LoginForm } from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <div className="container mx-auto py-12 px-4 flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md">
        <LoginForm />
      </div>
    </div>
  );
}
