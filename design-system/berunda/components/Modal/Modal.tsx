import { useEffect, useRef, useCallback, useState, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import clsx from 'clsx';
import { X } from 'lucide-react';
import styles from './Modal.module.css';

type ModalSize = 'sm' | 'md' | 'lg' | 'fullscreen';

const sizeClassMap: Record<ModalSize, string> = {
  sm: styles.sizeSm,
  md: styles.sizeMd,
  lg: styles.sizeLg,
  fullscreen: styles.sizeFullscreen,
};

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
  footerContent?: ReactNode;
  size?: ModalSize;
}

export default function Modal({
  isOpen,
  onClose,
  title,
  children,
  footerContent,
  size = 'md',
}: ModalProps) {
  const [closing, setClosing] = useState(false);
  const overlayRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<HTMLElement | null>(null);

  const handleClose = useCallback(() => {
    setClosing(true);
    setTimeout(() => {
      setClosing(false);
      onClose();
    }, 150);
  }, [onClose]);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        handleClose();
      }
      if (e.key === 'Tab' && contentRef.current) {
        const focusable = contentRef.current.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
        );
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    },
    [handleClose],
  );

  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement as HTMLElement;
      document.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';

      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        document.body.style.overflow = '';
        previousActiveElement.current?.focus();
      };
    }
  }, [isOpen, handleKeyDown]);

  if (!isOpen && !closing) return null;

  return createPortal(
    <div
      ref={overlayRef}
      data-testid="modal-overlay"
      className={clsx(styles.overlay, closing && styles.overlayClosing)}
      onClick={(e) => {
        if (e.target === overlayRef.current) handleClose();
      }}
      aria-hidden="true"
    >
      <div
        ref={contentRef}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        data-testid="modal-content"
        className={clsx(styles.content, sizeClassMap[size], closing && styles.contentClosing)}
      >
        {title && (
          <div className={styles.header}>
            <h2 className={styles.title}>{title}</h2>
            <button
              onClick={handleClose}
              className={styles.closeButton}
              data-testid="modal-close"
              aria-label="Close modal"
            >
              <X size={20} />
            </button>
          </div>
        )}

        <div className={styles.body} data-testid="modal-body">
          {children}
        </div>

        {footerContent && (
          <div className={styles.footer} data-testid="modal-footer">
            {footerContent}
          </div>
        )}
      </div>
    </div>,
    document.body,
  );
}
