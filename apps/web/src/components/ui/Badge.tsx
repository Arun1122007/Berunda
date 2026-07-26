import clsx from "clsx";

type BadgeVariant =
  | "default"
  | "secondary"
  | "success"
  | "warning"
  | "danger"
  | "info";

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
}

const variantStyles: Record<BadgeVariant, string> = {
  default: "bg-surface-700 text-surface-300",
  secondary: "bg-surface-600 text-surface-200",
  success: "bg-green-900/50 text-green-400",
  warning: "bg-yellow-900/50 text-yellow-400",
  danger: "bg-red-900/50 text-red-400",
  info: "bg-berunda-900/50 text-berunda-400",
};

export default function Badge({
  children,
  variant = "default",
  className,
}: BadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        variantStyles[variant],
        className
      )}
    >
      {children}
    </span>
  );
}
