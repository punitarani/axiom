"use client";

import {
  AlertCircle,
  CheckCircle,
  ExternalLink,
  Loader2,
  LogOut,
  RefreshCcw,
  RotateCcw,
  Unlink,
  User,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { env } from "@/env";
import { useAuth } from "@/hooks/useAuth";

interface Connection {
  name: string;
  connected: boolean;
  available: boolean;
  reason?: string;
}

interface ConnectionStatus {
  connections: Record<string, Connection>;
}

export default function Profile() {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const [signingOut, setSigningOut] = useState(false);
  const [connections, setConnections] = useState<Record<string, Connection>>(
    {},
  );
  const [schwabLoading, setSchwabLoading] = useState<
    "connect" | "disconnect" | "reset" | null
  >(null);
  const [_fetchingStatus, setFetchingStatus] = useState(false);

  const fetchConnectionStatus = useCallback(async () => {
    if (!user) return;

    try {
      setFetchingStatus(true);
      const response = await fetch(
        `${env.NEXT_PUBLIC_API_URL}/connections/status`,
        {
          mode: "cors",
          credentials: "include",
        },
      );

      if (response.ok) {
        const data: ConnectionStatus = await response.json();
        setConnections(data.connections);
      }
    } catch (error) {
      console.error("Failed to fetch connection status:", error);
    } finally {
      setFetchingStatus(false);
    }
  }, [user]);

  useEffect(() => {
    if (user?.id) {
      fetchConnectionStatus();
    }
  }, [user?.id, fetchConnectionStatus]);

  const handleConnect = async () => {
    setSchwabLoading("connect");

    try {
      const response = await fetch(
        `${env.NEXT_PUBLIC_API_URL}/connect/schwab`,
        {
          method: "POST",
          mode: "cors",
          credentials: "include",
        },
      );

      if (response.ok) {
        const data = await response.json();
        if (data.auth_url) {
          window.location.href = data.auth_url;
        } else if (data.connected) {
          await fetchConnectionStatus();
        }
      }
    } catch (error) {
      console.error("Failed to connect Schwab:", error);
    } finally {
      setSchwabLoading(null);
    }
  };

  const handleDisconnect = async () => {
    setSchwabLoading("disconnect");

    try {
      const response = await fetch(
        `${env.NEXT_PUBLIC_API_URL}/disconnect/schwab`,
        {
          method: "DELETE",
          mode: "cors",
          credentials: "include",
        },
      );

      if (response.ok) {
        await fetchConnectionStatus();
      }
    } catch (error) {
      console.error("Failed to disconnect Schwab:", error);
    } finally {
      setSchwabLoading(null);
    }
  };

  const handleReset = async () => {
    setSchwabLoading("reset");

    try {
      const response = await fetch(`${env.NEXT_PUBLIC_API_URL}/reset/schwab`, {
        method: "POST",
        mode: "cors",
        credentials: "include",
      });

      if (response.ok) {
        await fetchConnectionStatus();
      }
    } catch (error) {
      console.error("Failed to reset Schwab:", error);
    } finally {
      setSchwabLoading(null);
    }
  };

  const handleSignOut = async () => {
    try {
      setSigningOut(true);
      await signOut();
      router.push("/");
    } catch (error) {
      console.error("Error signing out:", error);
    } finally {
      setSigningOut(false);
    }
  };

  if (!user) {
    return (
      <div className="container mx-auto py-12 px-4 max-w-4xl">
        <div className="text-center space-y-6">
          <Card className="max-w-md mx-auto">
            <CardHeader>
              <CardTitle>Get Started</CardTitle>
              <CardDescription>
                Sign in to connect your Charles Schwab account
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild className="w-full">
                <Link href="/login">Sign In</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="grid gap-6 md:grid-cols-2 grid-cols-1">
        {/* Profile Card */}
        <Card className="h-[220px] flex flex-col justify-between">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Profile
              </CardTitle>
              <Badge variant="default" className="flex items-center gap-1">
                <CheckCircle className="h-3 w-3" />
                Active
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-1">
            <p className="font-medium">{user.email}</p>
            <p className="text-sm text-muted-foreground">
              Member since {new Date(user.created_at).toLocaleDateString()}
            </p>
          </CardContent>
          <CardFooter>
            <Button
              onClick={handleSignOut}
              variant="outline"
              className="w-full"
              disabled={signingOut}
            >
              {signingOut ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Signing out...
                </>
              ) : (
                <>
                  <LogOut className="mr-2 h-4 w-4" />
                  Sign Out
                </>
              )}
            </Button>
          </CardFooter>
        </Card>

        {/* Charles Schwab Connection Card */}
        <Card className="h-[220px] flex flex-col justify-between">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <ExternalLink className="h-5 w-5" />
                Charles Schwab
              </CardTitle>
              <div className="flex items-center gap-2">
                {!connections.schwab?.connected &&
                  (schwabLoading !== null ? (
                    <div className="p-2">
                      <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                    </div>
                  ) : (
                    <Button
                      onClick={handleReset}
                      size="sm"
                      variant="ghost"
                      className="p-2"
                      title="Reset connection and clear stored auth data"
                    >
                      <RefreshCcw className="h-4 w-4" />
                    </Button>
                  ))}
                {connections.schwab?.connected ? (
                  <Badge variant="default" className="flex items-center gap-1">
                    <CheckCircle className="h-3 w-3" />
                    Connected
                  </Badge>
                ) : (
                  <Badge
                    variant="secondary"
                    className="flex items-center gap-1"
                  >
                    <AlertCircle className="h-3 w-3" />
                    Disconnected
                  </Badge>
                )}
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-1">
            <p className="font-medium">
              {connections.schwab && !connections.schwab.available
                ? connections.schwab.reason || "Not available"
                : connections.schwab?.connected
                  ? "Account connected and ready"
                  : "Connect your brokerage account"}
            </p>
            <p className="text-sm text-muted-foreground">
              {connections.schwab?.connected
                ? "Trading enabled"
                : "Authorization required"}
            </p>
          </CardContent>
          <CardFooter>
            {connections.schwab?.available === false ? (
              <Button disabled className="w-full" variant="outline">
                <AlertCircle className="mr-2 h-4 w-4" />
                Not Available
              </Button>
            ) : connections.schwab?.connected ? (
              <div className="flex gap-2 w-full">
                <Button
                  onClick={handleConnect}
                  disabled={schwabLoading !== null}
                  variant="outline"
                  className="flex-1"
                >
                  {schwabLoading === "connect" ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Re-connecting...
                    </>
                  ) : (
                    <>
                      <RotateCcw className="mr-2 h-4 w-4" />
                      Re-connect
                    </>
                  )}
                </Button>
                <Button
                  onClick={handleDisconnect}
                  disabled={schwabLoading !== null}
                  variant="destructive"
                  className="flex-1"
                >
                  {schwabLoading === "disconnect" ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Disconnecting...
                    </>
                  ) : (
                    <>
                      <Unlink className="mr-2 h-4 w-4" />
                      Disconnect
                    </>
                  )}
                </Button>
              </div>
            ) : (
              <Button
                onClick={handleConnect}
                disabled={schwabLoading !== null}
                className="w-full"
              >
                {schwabLoading === "connect" ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Connecting...
                  </>
                ) : (
                  <>
                    <ExternalLink className="mr-2 h-4 w-4" />
                    Connect
                  </>
                )}
              </Button>
            )}
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
