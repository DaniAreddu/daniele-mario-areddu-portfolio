import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

/**
 * A render crash anywhere in the admin area must never present as a silent
 * form reset or a blank white screen — it should say so plainly and offer a
 * way back, since losing in-progress edits without any explanation is the
 * worst possible failure mode for a CMS.
 */
export class AdminErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Admin UI crashed:", error, info.componentStack);
  }

  render() {
    if (this.state.error) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-paper-warm px-4">
          <div className="max-w-sm rounded-2xl border border-red-300 bg-red-50 p-6 text-center">
            <p className="font-serif text-xl text-ink">Something went wrong.</p>
            <p className="mt-2 text-sm text-ink-soft">
              An unexpected error occurred in the admin interface. Any unsaved changes on this
              screen may have been lost.
            </p>
            <a href="/admin" className="mt-4 inline-block text-cobalt underline">
              Back to dashboard
            </a>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
