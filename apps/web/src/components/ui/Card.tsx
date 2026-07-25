import { HTMLAttributes, forwardRef } from "react";
import clsx from "clsx";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  header?: React.ReactNode;
  footer?: React.ReactNode;
  hover?: boolean;
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ header, footer, children, className, hover, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={clsx(
          "rounded-xl border border-surface-700 bg-surface-800 shadow-lg transition-all duration-200",
          hover && "cursor-pointer hover:-translate-y-0.5 hover:border-berunda-700 hover:shadow-berunda-900/20 hover:shadow-xl",
          className
        )}
        {...props}
      >
        {header && (
          <div className="border-b border-surface-700 px-6 py-4">
            {header}
          </div>
        )}
        {children && <div className="px-6 py-4">{children}</div>}
        {footer && (
          <div className="border-t border-surface-700 px-6 py-4">
            {footer}
          </div>
        )}
      </div>
    );
  }
);

Card.displayName = "Card";
export default Card;
