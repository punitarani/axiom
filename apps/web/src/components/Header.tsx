import Link from "next/link";
import { memo } from "react";
import { User } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

const Header = memo(() => {
  return (
    <header className="border-b bg-background">
      <div className="container mx-auto px-4 h-14 flex items-center justify-between">
        <Link
          href="/"
          className="text-xl font-bold hover:opacity-80 transition-opacity"
        >
          Axiom
        </Link>

        <Link href="/profile">
          <Avatar className="h-8 w-8 cursor-pointer hover:ring-2 hover:ring-ring hover:ring-offset-2 transition-all">
            <AvatarFallback>
              <User className="h-4 w-4" />
            </AvatarFallback>
          </Avatar>
        </Link>
      </div>
    </header>
  );
});

Header.displayName = "Header";

export default Header;
