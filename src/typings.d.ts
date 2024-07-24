// src/typings.d.ts
// interface Window {
//     dataLayer: any[];
//     gtag: (...args: any[]) => void;
//   }
  
  // src/typings.d.ts
interface Window {
    dataLayer: any[];
    gtag: (command: string, targetId: string, config?: { [key: string]: any }) => void;
  }
  