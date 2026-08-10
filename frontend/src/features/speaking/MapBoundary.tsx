import { Component, type ReactNode } from "react";

interface MapBoundaryProps {
  fallback: ReactNode;
  children: ReactNode;
}

interface MapBoundaryState {
  hasError: boolean;
}

/** Catches runtime failures from the MapLibre bundle or tile loading and
 * swaps in the accessible list fallback instead of a blank, broken section. */
export class MapBoundary extends Component<MapBoundaryProps, MapBoundaryState> {
  state: MapBoundaryState = { hasError: false };

  static getDerivedStateFromError(): MapBoundaryState {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}
