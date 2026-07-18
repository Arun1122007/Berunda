import { Component, ErrorInfo, ReactNode } from "react";
import Button from "./Button";
import { AlertTriangle, RefreshCw } from "lucide-react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  private handleRetry = (): void => {
    this.setState({ hasError: false, error: null });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="flex min-h-[400px] items-center justify-center">
          <div className="text-center">
            <AlertTriangle className="mx-auto mb-4 h-12 w-12 text-red-400" />
            <h2 className="mb-2 text-xl font-semibold text-surface-100">
              Something went wrong
            </h2>
            <p className="mb-6 text-sm text-surface-400">
              {this.state.error?.message || "An unexpected error occurred"}
            </p>
            <Button onClick={this.handleRetry} icon={<RefreshCw size={16} />}>
              Try Again
            </Button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
