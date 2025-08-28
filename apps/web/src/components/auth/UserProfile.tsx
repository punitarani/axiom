"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

export function UserProfile() {
  const { user, signOut, loading } = useAuth();
  const router = useRouter();
  const [signingOut, setSigningOut] = useState(false);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return null;
  }

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

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Welcome!</CardTitle>
        <CardDescription>You are signed in as {user.email}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center space-x-4">
          <Avatar>
            <AvatarFallback>
              {user.email?.[0]?.toUpperCase() || "U"}
            </AvatarFallback>
          </Avatar>
          <div>
            <p className="text-sm font-medium">{user.email}</p>
            <p className="text-xs text-muted-foreground">
              User ID: {user.id.slice(0, 8)}...
            </p>
          </div>
        </div>
        <Button
          onClick={handleSignOut}
          variant="outline"
          className="w-full"
          disabled={signingOut}
        >
          {signingOut ? "Signing out..." : "Sign Out"}
        </Button>
      </CardContent>
    </Card>
  );
}
