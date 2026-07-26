import { ButtonHTMLAttributes, forwardRef } from 'react';
import clsx from 'clsx';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';
import styles from './Button.module.css';

type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
type ButtonSize = 'sm' | 'md' | 'lg';
type IconPosition = 'left' | 'right';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: IconPosition;
  fullWidth?: boolean;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      loading = false,
      disabled,
      icon,
      iconPosition = 'left',
      fullWidth = false,
      children,
      className,
      type = 'button',
      ...props
    },
    ref,
  ) => {
    return (
      <button
        ref={ref}
        type={type}
        data-testid="button"
        disabled={disabled || loading}
        aria-disabled={disabled || loading}
        aria-busy={loading}
        className={clsx(
          styles.button,
          styles[variant],
          styles[size],
          fullWidth && styles.fullWidth,
          loading && styles.loading,
          className,
        )}
        {...props}
      >
        {loading ? (
          <LoadingSpinner size={size === 'lg' ? 'md' : 'sm'} />
        ) : icon && iconPosition === 'left' ? (
          <span className={styles.iconLeft} data-testid="button-icon-left">{icon}</span>
        ) : null}
        {children && <span>{children}</span>}
        {!loading && icon && iconPosition === 'right' && (
          <span className={styles.iconRight} data-testid="button-icon-right">{icon}</span>
        )}
      </button>
    );
  },
);

Button.displayName = 'Button';
export default Button;
