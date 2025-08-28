"use client";

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

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return null;
  }

  const handleSignOut = async () => {
    await signOut();
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
        <Button onClick={handleSignOut} variant="outline" className="w-full">
          Sign Out
        </Button>
      </CardContent>
    </Card>
  );
}
