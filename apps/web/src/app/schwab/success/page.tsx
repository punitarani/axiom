"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle, ArrowLeft } from "lucide-react";

export default function SchwabSuccessPage() {
  const router = useRouter();

  useEffect(() => {
    // Auto-redirect after 5 seconds
    const timer = setTimeout(() => {
      router.push("/schwab");
    }, 5000);

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <div className="container mx-auto py-8 max-w-2xl">
      <Card>
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
            <CheckCircle className="h-6 w-6 text-green-600" />
          </div>
          <CardTitle className="text-green-800">Schwab Account Connected!</CardTitle>
          <CardDescription>
            Your Charles Schwab account has been successfully connected and secured.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center space-y-4">
          <p className="text-sm text-muted-foreground">
            Your trading tokens have been securely stored and encrypted. 
            You can now access Schwab trading features.
          </p>
          
          <div className="space-y-2">
            <Button onClick={() => router.push("/schwab")} className="w-full">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Return to Schwab Settings
            </Button>
            
            <Button 
              onClick={() => router.push("/")} 
              variant="outline" 
              className="w-full"
            >
              Go to Dashboard
            </Button>
          </div>
          
          <p className="text-xs text-muted-foreground">
            Redirecting automatically in 5 seconds...
          </p>
        </CardContent>
      </Card>
    </div>
  );
}