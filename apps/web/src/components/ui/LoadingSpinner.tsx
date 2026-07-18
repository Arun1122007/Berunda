import clsx from "clsx";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizeStyles = {
  sm: "h-4 w-4 border-2",
  md: "h-8 w-8 border-3",
  lg: "h-12 w-12 border-4",
};

export default function LoadingSpinner({
  size = "md",
  className,
}: LoadingSpinnerProps) {
  return (
    <div
      className={clsx(
        "animate-spin rounded-full border-berunda-600 border-t-transparent",
        sizeStyles[size],
        className
      )}
      role="status"
      aria-label="Loading"
    />
  );
}
