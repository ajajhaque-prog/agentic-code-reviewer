// bad_ts.ts
// TypeScript sample with type and TODO issues

function addNumbers(a: number, b: string): number {
  // TODO: Fix type mismatch
  return a + parseInt(b);
}

addNumbers(10, "20");
