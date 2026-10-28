import js from "@eslint/js";
import globals from "globals";
import hooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["**/node_modules/**", "**/.next/**", "**/.expo/**", "**/dist/**", "**/coverage/**", "**/schema.d.ts", "**/next-env.d.ts", "**/expo-env.d.ts"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  { languageOptions: { globals: { ...globals.node, ...globals.browser, ...globals.jest } } },
  { files: ["**/*.{ts,tsx}"], plugins: { "react-hooks": hooks }, rules: { ...hooks.configs.recommended.rules, "@typescript-eslint/no-explicit-any": "error" } },
);
