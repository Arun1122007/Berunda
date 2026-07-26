import clsx from 'clsx';
import styles from './Badge.module.css';

type BadgeVariant = 'default' | 'success' | 'warning' | 'error' | 'info';
type BadgeSize = 'sm' | 'md';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  size?: BadgeSize;
  className?: string;
}

export default function Badge({
  children,
  variant = 'default',
  size = 'md',
  className,
}: BadgeProps) {
  return (
    <span
      data-testid="badge"
      className={clsx(styles.badge, styles[variant], styles[size], className)}
    >
      {children}
    </span>
  );
}
