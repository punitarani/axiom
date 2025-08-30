"use client";

import { AlertCircle, ArrowLeft, CheckCircle, Loader2 } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

type CallbackState = "loading" | "success" | "error";

function OAuthCallback() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [state, setState] = useState<CallbackState>("loading");
  const [error, setError] = useState<string>("");
  const [connectionType, setConnectionType] = useState<string>("");
  const [countdown, setCountdown] = useState<number>(3);

  useEffect(() => {
    const handleOAuthCallback = () => {
      const successParam = searchParams.get("success");
      const errorParam = searchParams.get("error");
      const connection = searchParams.get("connection");

      // Set connection type
      if (connection) {
        setConnectionType(
          connection.charAt(0).toUpperCase() + connection.slice(1),
        );
      }

      if (errorParam) {
        setError(errorParam);
        setState("error");
        return;
      }

      if (successParam === "true") {
        setState("success");

        // Start countdown timer and redirect
        let timeLeft = 3;
        setCountdown(timeLeft);
        
        const timer = setInterval(() => {
          timeLeft -= 1;
          setCountdown(timeLeft);
          
          if (timeLeft <= 0) {
            clearInterval(timer);
            router.push("/");
          }
        }, 1000);
      } else {
        setError("Unknown callback state");
        setState("error");
      }
    };

    handleOAuthCallback();
  }, [searchParams, router]);

  const renderContent = () => {
    switch (state) {
      case "loading":
        return (
          <Card className="border-0 shadow-lg">
            <CardHeader className="text-center pb-4">
              <div className="mx-auto mb-3 flex h-10 w-10 items-center justify-center">
                <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
              </div>
              <CardTitle className="text-lg">Connecting Account</CardTitle>
              <CardDescription className="text-sm">
                Securely processing your {connectionType || "broker"} connection
              </CardDescription>
            </CardHeader>
          </Card>
        );

      case "success":
        return (
          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                <CheckCircle className="h-6 w-6 text-green-600" />
              </div>
              <CardTitle className="text-green-800">
                {connectionType} Account Connected!
              </CardTitle>
              <CardDescription>
                Your account has been successfully connected and secured.
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="text-sm text-muted-foreground">
                Your trading tokens have been securely stored and encrypted. You
                can now access trading features.
              </p>

              <div className="space-y-2">
                <Button onClick={() => router.push("/")} className="w-full">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Return to Dashboard
                </Button>
              </div>

              <p className="text-xs text-muted-foreground">
                Redirecting automatically in {countdown} second{countdown !== 1 ? 's' : ''}...
              </p>
            </CardContent>
          </Card>
        );

      case "error":
        return (
          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
                <AlertCircle className="h-6 w-6 text-red-600" />
              </div>
              <CardTitle className="text-red-800">Connection Failed</CardTitle>
              <CardDescription>
                There was an error connecting your account.
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="text-sm text-muted-foreground">{error}</p>

              <div className="space-y-2">
                <Button onClick={() => router.push("/")} className="w-full">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Return to Dashboard
                </Button>
              </div>

              <p className="text-xs text-muted-foreground">
                You can try connecting again from the dashboard.
              </p>
            </CardContent>
          </Card>
        );
    }
  };

  return (
    <div className="container mx-auto py-8 max-w-2xl">{renderContent()}</div>
  );
}

export default function OAuthCallbackPage() {
  return (
    <Suspense
      fallback={
        <div className="container mx-auto py-8 max-w-2xl">
          <Card>
            <CardContent className="text-center py-8">
              <Loader2 className="h-6 w-6 animate-spin mx-auto" />
            </CardContent>
          </Card>
        </div>
      }
    >
      <OAuthCallback />
    </Suspense>
  );
}
