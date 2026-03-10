import { create } from "zustand";
import { persist } from "zustand/middleware";

interface MagicLinkState {
    magicLink: string | null;
    expiresAt: number | null;

    setMagicLink: (link: string) => void;
    clearMagicLink: () => void;
    isMagicLinkValid: () => boolean;
}

export const useMagicLinkStore = create<MagicLinkState>()(
    persist(
        (set, get) => ({
            magicLink: null,
            expiresAt: null,

            setMagicLink: (link: string) => {
                const expiresInMs = 20 * 60 * 1000;
                const expiresAt = Date.now() + expiresInMs;

                set({
                    magicLink: link,
                    expiresAt,
                });

                setTimeout(() => {
                    const currentExpiresAt = get().expiresAt;

                    if (currentExpiresAt && currentExpiresAt <= Date.now()) {
                        set({ magicLink: null, expiresAt: null });
                    }
                }, expiresInMs);
            },

            clearMagicLink: () => {
                set({ magicLink: null, expiresAt: null });
            },

            isMagicLinkValid: () => {
                const { magicLink, expiresAt} = get();

                return !!(magicLink && expiresAt && Date.now() < expiresAt);
            },
        }),
        {
            name: "magic-link-storage"
        }
    )
)