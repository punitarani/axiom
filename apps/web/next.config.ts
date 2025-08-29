import type { NextConfig } from "next";
import { env } from "@/env";

const nextConfig: NextConfig = {
  allowedDevOrigins: [env.NEXT_PUBLIC_API_URL],
};

export default nextConfig;
