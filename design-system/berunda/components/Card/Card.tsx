import { HTMLAttributes, forwardRef } from 'react';
import clsx from 'clsx';
import styles from './Card.module.css';

type CardVariant = 'default' | 'elevated' | 'outlined' | 'interactive';
type CardPadding = 'none' | 'sm' | 'md' | 'lg';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: CardVariant;
  padding?: CardPadding;
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ variant = 'default', padding = 'md', children, className, onClick, ...props }, ref) => {
    const isInteractive = variant === 'interactive' || onClick;
    return (
      <div
        ref={ref}
        data-testid="card"
        role={isInteractive ? 'button' : undefined}
        tabIndex={isInteractive ? 0 : undefined}
        onKeyDown={
          isInteractive
            ? (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  onClick?.(e as unknown as React.MouseEvent<HTMLDivElement>);
                }
              }
            : undefined
        }
        className={clsx(
          styles.card,
          styles[variant],
          padding !== 'md' && styles[`padding${padding.charAt(0).toUpperCase() + padding.slice(1)}` as keyof typeof styles],
          isInteractive && styles.interactive,
          className,
        )}
        onClick={onClick}
        {...props}
      >
        {children}
      </div>
    );
  },
);

Card.displayName = 'Card';

interface CardSubComponentProps {
  children: React.ReactNode;
  className?: string;
}

const CardHeader = forwardRef<HTMLDivElement, CardSubComponentProps>(
  ({ children, className }, ref) => (
    <div ref={ref} data-testid="card-header" className={clsx(styles.header, className)}>
      {children}
    </div>
  ),
);
CardHeader.displayName = 'CardHeader';

const CardBody = forwardRef<HTMLDivElement, CardSubComponentProps>(
  ({ children, className }, ref) => (
    <div ref={ref} data-testid="card-body" className={clsx(styles.body, className)}>
      {children}
    </div>
  ),
);
CardBody.displayName = 'CardBody';

const CardFooter = forwardRef<HTMLDivElement, CardSubComponentProps>(
  ({ children, className }, ref) => (
    <div ref={ref} data-testid="card-footer" className={clsx(styles.footer, className)}>
      {children}
    </div>
  ),
);
CardFooter.displayName = 'CardFooter';

export default Card;
export { CardHeader, CardBody, CardFooter };
