declare module 'asciinema-player' {
  interface PlayerOptions {
    speed?: number;
    cols?: number;
    rows?: number;
    autoPlay?: boolean;
    loop?: boolean;
    fit?: 'width' | 'height' | 'both' | 'none';
    theme?: string;
    terminalFontFamily?: string;
    terminalFontSize?: string;
  }

  interface Player {
    dispose(): void;
    play(): void;
    pause(): void;
  }

  export function create(src: string, container: HTMLElement, options?: PlayerOptions): Player;
}
