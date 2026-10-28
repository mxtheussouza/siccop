import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import LoginPage from "../src/app/login/page";
import { messages } from "../src/i18n";

describe("bootstrap login boundary", () => {
  it("announces unavailable authentication and does not collect credentials", () => {
    render(<LoginPage />);
    expect(
      screen.getByRole("heading", { name: messages.login.title }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: messages.login.action }),
    ).toBeDisabled();
    expect(screen.getByRole("button")).toHaveAccessibleDescription(
      messages.login.description,
    );
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
  });
});
