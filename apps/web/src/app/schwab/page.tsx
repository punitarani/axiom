"use client";

import { AlertCircle, CheckCircle, ExternalLink, Loader2 } from "lucide-react";
import { useState } from "react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { env } from "@/env";
import { useAuth } from "@/hooks/useAuth";

export default function SchwabConnectionPage() {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleConnectSchwab = async () => {
    if (!user) {
      setError("Please log in to connect your Schwab account");
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(
        `${env.NEXT_PUBLIC_API_URL}/connect/schwab`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        },
      );

      if (!response.ok) {
        if (response.status === 403) {
          throw new Error(
            "Access denied. You don't have permission to connect Schwab accounts.",
          );
        }
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to connect Schwab account");
      }

      const data = await response.json();

      if (data.connected) {
        setSuccess(data.message);
      } else if (data.auth_url) {
        // Redirect to Schwab OAuth
        window.location.href = data.auth_url;
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "An unexpected error occurred",
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnectSchwab = async () => {
    if (!user) {
      setError("Please log in to disconnect your Schwab account");
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(
        `${env.NEXT_PUBLIC_API_URL}/disconnect/schwab`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        },
      );

      if (!response.ok) {
        if (response.status === 403) {
          throw new Error(
            "Access denied. You don't have permission to disconnect Schwab accounts.",
          );
        }
        const errorData = await response.json();
        throw new Error(
          errorData.error || "Failed to disconnect Schwab account",
        );
      }

      const data = await response.json();
      setSuccess(data.message);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "An unexpected error occurred",
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="container mx-auto py-8">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5 text-amber-500" />
              Authentication Required
            </CardTitle>
            <CardDescription>
              Please log in to access Schwab account connection.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ExternalLink className="h-6 w-6 text-blue-600" />
            Charles Schwab Connection
          </CardTitle>
          <CardDescription>
            Connect your Charles Schwab account to access trading features. Only
            authorized users can connect trading accounts.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert>
              <CheckCircle className="h-4 w-4" />
              <AlertDescription>{success}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-3">
            <Button
              onClick={handleConnectSchwab}
              disabled={isLoading}
              className="w-full"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Connecting...
                </>
              ) : (
                <>
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Connect Schwab Account
                </>
              )}
            </Button>

            <Button
              onClick={handleDisconnectSchwab}
              disabled={isLoading}
              variant="outline"
              className="w-full"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Disconnecting...
                </>
              ) : (
                "Disconnect Schwab Account"
              )}
            </Button>
          </div>

          <div className="text-sm text-muted-foreground space-y-2">
            <p>
              <strong>Important:</strong>
            </p>
            <ul className="list-disc list-inside space-y-1">
              <li>You'll be redirected to Schwab's secure login page</li>
              <li>Your credentials are never stored on our servers</li>
              <li>Only authorized trading tokens are stored securely</li>
              <li>You can disconnect at any time</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
