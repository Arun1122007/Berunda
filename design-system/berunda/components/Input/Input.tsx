import {
  InputHTMLAttributes,
  TextareaHTMLAttributes,
  forwardRef,
  useId,
} from 'react';
import clsx from 'clsx';
import styles from './Input.module.css';

type InputType = 'text' | 'email' | 'password' | 'number' | 'search';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  textarea?: false;
}

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  textarea: true;
}

type CombinedProps = InputProps | TextareaProps;

const Input = forwardRef<HTMLInputElement | HTMLTextAreaElement, CombinedProps>(
  (
    {
      label,
      error,
      helperText,
      leftIcon,
      rightIcon,
      fullWidth = true,
      textarea = false,
      className,
      id: externalId,
      disabled,
      readOnly,
      ...props
    },
    ref,
  ) => {
    const generatedId = useId();
    const inputId = externalId || generatedId;
    const errorId = `${inputId}-error`;
    const helperId = `${inputId}-helper`;

    const wrapperClassName = clsx(
      styles.wrapper,
      fullWidth && styles.fullWidth,
      error && styles.hasError,
      leftIcon && styles.hasLeftIcon,
      rightIcon && styles.hasRightIcon,
    );

    const inputClassName = clsx(
      styles.input,
      textarea && styles.textarea,
      readOnly && styles.readonly,
      className,
    );

    const sharedProps = {
      id: inputId,
      'data-testid': 'input',
      'aria-invalid': error ? true as const : undefined,
      'aria-describedby': error ? errorId : helperText ? helperId : undefined,
      disabled,
      readOnly,
      className: inputClassName,
    };

    return (
      <div className={wrapperClassName}>
        {label && (
          <label htmlFor={inputId} className={styles.label} data-testid="input-label">
            {label}
          </label>
        )}

        <div className={styles.inputContainer}>
          {leftIcon && (
            <span className={styles.iconLeft} data-testid="input-icon-left">
              {leftIcon}
            </span>
          )}

          {textarea ? (
            <textarea
              ref={ref as React.Ref<HTMLTextAreaElement>}
              {...(sharedProps as TextareaHTMLAttributes<HTMLTextAreaElement>)}
              {...(props as TextareaHTMLAttributes<HTMLTextAreaElement>)}
            />
          ) : (
            <input
              ref={ref as React.Ref<HTMLInputElement>}
              {...(sharedProps as InputHTMLAttributes<HTMLInputElement>)}
              {...(props as InputHTMLAttributes<HTMLInputElement>)}
            />
          )}

          {rightIcon && (
            <span className={styles.iconRight} data-testid="input-icon-right">
              {rightIcon}
            </span>
          )}
        </div>

        {error && (
          <span id={errorId} role="alert" className={styles.errorMessage} data-testid="input-error">
            {error}
          </span>
        )}

        {!error && helperText && (
          <span id={helperId} className={styles.helperText} data-testid="input-helper">
            {helperText}
          </span>
        )}
      </div>
    );
  },
);

Input.displayName = 'Input';

interface InputLabelProps {
  children: React.ReactNode;
  htmlFor?: string;
  className?: string;
}

const InputLabel = ({ children, htmlFor, className }: InputLabelProps) => (
  <label htmlFor={htmlFor} className={clsx(styles.label, className)} data-testid="input-label-component">
    {children}
  </label>
);

interface InputHelperTextProps {
  children: React.ReactNode;
  className?: string;
}

const InputHelperText = ({ children, className }: InputHelperTextProps) => (
  <span className={clsx(styles.helperText, className)} data-testid="input-helper-component">
    {children}
  </span>
);

interface InputErrorMessageProps {
  children: React.ReactNode;
  className?: string;
}

const InputErrorMessage = ({ children, className }: InputErrorMessageProps) => (
  <span role="alert" className={clsx(styles.errorMessage, className)} data-testid="input-error-component">
    {children}
  </span>
);

export default Input;
export { InputLabel, InputHelperText, InputErrorMessage };
