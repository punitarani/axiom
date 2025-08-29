import { type NextRequest, NextResponse } from "next/server";
import { env } from "@/env";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");
  const state = searchParams.get("state");
  const error = searchParams.get("error");

  // Handle OAuth errors
  if (error) {
    return NextResponse.redirect(
      new URL(
        `/oauth/callback?error=${encodeURIComponent(error)}&connection=schwab`,
        env.NEXT_PUBLIC_APP_URL,
      ),
    );
  }

  // Validate required parameters
  if (!code || !state) {
    return NextResponse.redirect(
      new URL(
        "/oauth/callback?error=Missing%20authorization%20code%20or%20state&connection=schwab",
        env.NEXT_PUBLIC_APP_URL,
      ),
    );
  }

  try {
    // Forward the callback to the backend
    const backendResponse = await fetch(
      `${env.NEXT_PUBLIC_API_URL}/api/auth/schwab/callback?code=${encodeURIComponent(code)}&state=${encodeURIComponent(state)}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      },
    );

    if (!backendResponse.ok) {
      throw new Error(`Backend returned ${backendResponse.status}`);
    }

    // If backend processed successfully, redirect to success
    return NextResponse.redirect(
      new URL(
        "/oauth/callback?success=true&connection=schwab",
        env.NEXT_PUBLIC_APP_URL,
      ),
    );
  } catch (error) {
    // Redirect to error page with error message
    const errorMessage =
      error instanceof Error ? error.message : "Unknown error";
    return NextResponse.redirect(
      new URL(
        `/oauth/callback?error=${encodeURIComponent(errorMessage)}&connection=schwab`,
        env.NEXT_PUBLIC_APP_URL,
      ),
    );
  }
}
