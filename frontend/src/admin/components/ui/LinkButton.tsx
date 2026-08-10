import { Link, type LinkProps } from "react-router-dom";

import { buttonClassName, type ButtonVariant } from "@/admin/components/ui/buttonStyles";

interface LinkButtonProps extends LinkProps {
  variant?: ButtonVariant;
}

export function LinkButton({ variant = "primary", className, ...props }: LinkButtonProps) {
  return <Link className={buttonClassName(variant, className)} {...props} />;
}
