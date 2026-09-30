import { NextResponse, type NextRequest } from "next/server";

// Derive language from the route, never from caller-supplied headers or preferences.
// Ordinary locale anchors perform document navigation, refreshing the root layout.
export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname.replace(/\/$/, "");
  const languages: Record<string, string> = {
    "/de": "de", "/es": "es", "/pt": "pt-BR", "/fr": "fr",
  };
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-akashicnet-document-language", languages[pathname] ?? "en");
  return NextResponse.next({ request: { headers: requestHeaders } });
}

export const config = {
  matcher: ["/((?!api/|_next/|images/|favicon.ico).*)"],
};
