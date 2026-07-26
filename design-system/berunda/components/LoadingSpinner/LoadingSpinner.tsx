import clsx from 'clsx';
import styles from './LoadingSpinner.module.css';

type SpinnerSize = 'sm' | 'md' | 'lg';

interface LoadingSpinnerProps {
  size?: SpinnerSize;
  label?: string;
  className?: string;
}

export default function LoadingSpinner({
  size = 'md',
  label,
  className,
}: LoadingSpinnerProps) {
  return (
    <div
      role="status"
      aria-label={label || 'Loading'}
      data-testid="loading-spinner"
      className={clsx(styles.spinner, styles[size], className)}
    >
      <div className={styles.anim} />
      {label && <span className={styles.label}>{label}</span>}
    </div>
  );
}
