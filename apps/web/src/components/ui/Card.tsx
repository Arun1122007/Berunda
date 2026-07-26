import React, { HTMLAttributes, forwardRef } from "react";
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

const CardHeader = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={clsx("flex flex-col space-y-1.5 border-b border-surface-700 px-6 py-4", className)} {...props} />
  )
);
CardHeader.displayName = "CardHeader";

const CardTitle = forwardRef<HTMLParagraphElement, HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={clsx("font-semibold leading-none tracking-tight text-surface-100", className)} {...props} />
  )
);
CardTitle.displayName = "CardTitle";

const CardContent = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={clsx("px-6 py-4", className)} {...props} />
  )
);
CardContent.displayName = "CardContent";

const CardFooter = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={clsx("flex items-center border-t border-surface-700 px-6 py-4", className)} {...props} />
  )
);
CardFooter.displayName = "CardFooter";

export default Card;
export { CardHeader, CardTitle, CardContent, CardFooter };
