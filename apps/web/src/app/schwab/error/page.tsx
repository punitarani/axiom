"use client";

import { AlertCircle, ArrowLeft, RefreshCw } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

function SchwabErrorContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const errorMessage =
    searchParams.get("message") ||
    "An unexpected error occurred during Schwab authentication";

  return (
    <div className="container mx-auto py-8 max-w-2xl">
      <Card>
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
            <AlertCircle className="h-6 w-6 text-red-600" />
          </div>
          <CardTitle className="text-red-800">Connection Failed</CardTitle>
          <CardDescription>
            There was an issue connecting your Charles Schwab account.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{errorMessage}</AlertDescription>
          </Alert>

          <div className="text-sm text-muted-foreground space-y-2">
            <p>
              <strong>Possible solutions:</strong>
            </p>
            <ul className="list-disc list-inside space-y-1">
              <li>Ensure you have valid Schwab developer credentials</li>
              <li>
                Check that the callback URL matches your Schwab app
                configuration
              </li>
              <li>Verify you completed the OAuth flow without canceling</li>
              <li>Try the connection process again</li>
            </ul>
          </div>

          <div className="space-y-2">
            <Button onClick={() => router.push("/schwab")} className="w-full">
              <RefreshCw className="mr-2 h-4 w-4" />
              Try Again
            </Button>

            <Button
              onClick={() => router.push("/")}
              variant="outline"
              className="w-full"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Go to Dashboard
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function SchwabErrorPage() {
  return (
    <Suspense fallback={null}>
      <SchwabErrorContent />
    </Suspense>
  );
}
