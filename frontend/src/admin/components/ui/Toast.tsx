import * as ToastPrimitive from "@radix-ui/react-toast";
import { clsx } from "clsx";
import { createContext, useCallback, useContext, useState, type ReactNode } from "react";

interface ToastMessage {
  id: number;
  title: string;
  description?: string;
  variant?: "default" | "error";
}

interface AdminToastContextValue {
  showToast: (toast: Omit<ToastMessage, "id">) => void;
}

const AdminToastContext = createContext<AdminToastContextValue | null>(null);

let nextToastId = 1;

export function AdminToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const showToast = useCallback((toast: Omit<ToastMessage, "id">) => {
    setToasts((current) => [...current, { ...toast, id: nextToastId++ }]);
  }, []);

  const dismiss = useCallback((id: number) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  return (
    <AdminToastContext.Provider value={{ showToast }}>
      <ToastPrimitive.Provider swipeDirection="right" duration={5000}>
        {children}
        {toasts.map((toast) => (
          <ToastPrimitive.Root
            key={toast.id}
            onOpenChange={(open) => {
              if (!open) dismiss(toast.id);
            }}
            className={clsx(
              "rounded-xl border p-4 shadow-lg",
              toast.variant === "error" ? "border-red-300 bg-red-50" : "border-ink/15 bg-paper",
            )}
          >
            <ToastPrimitive.Title className="text-sm font-medium text-ink">
              {toast.title}
            </ToastPrimitive.Title>
            {toast.description ? (
              <ToastPrimitive.Description className="mt-1 text-sm text-ink-soft">
                {toast.description}
              </ToastPrimitive.Description>
            ) : null}
          </ToastPrimitive.Root>
        ))}
        <ToastPrimitive.Viewport className="fixed bottom-4 right-4 z-50 flex w-96 max-w-[calc(100vw-2rem)] flex-col gap-2 outline-none" />
      </ToastPrimitive.Provider>
    </AdminToastContext.Provider>
  );
}

export function useAdminToast(): AdminToastContextValue {
  const context = useContext(AdminToastContext);
  if (!context) {
    throw new Error("useAdminToast must be used within an AdminToastProvider");
  }
  return context;
}
