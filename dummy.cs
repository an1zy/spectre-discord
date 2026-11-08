using System;
using System.Runtime.InteropServices;

class DummyProgram {
    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    static extern IntPtr CreateWindowEx(
        uint dwExStyle, string lpClassName, string lpWindowName, uint dwStyle,
        int x, int y, int nWidth, int nHeight, IntPtr hWndParent, IntPtr hMenu,
        IntPtr hInstance, IntPtr lpParam);

    [DllImport("user32.dll")]
    static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    static extern bool GetMessage(out MSG lpMsg, IntPtr hWnd, uint wMsgFilterMin, uint wMsgFilterMax);

    [DllImport("user32.dll")]
    static extern bool TranslateMessage([In] ref MSG lpMsg);

    [DllImport("user32.dll")]
    static extern IntPtr DispatchMessage([In] ref MSG lpMsg);

    [StructLayout(LayoutKind.Sequential)]
    struct MSG {
        public IntPtr hwnd;
        public uint message;
        public IntPtr wParam;
        public IntPtr lParam;
        public uint time;
        public int pt_x;
        public int pt_y;
    }

    const uint WS_EX_TOOLWINDOW = 0x00000080;
    const uint WS_EX_NOACTIVATE = 0x08000000;
    const uint WS_POPUP = 0x80000000;
    const int SW_SHOWNA = 8;

    [STAThread]
    static void Main(string[] args) {
        string title = (args.Length > 0 && !string.IsNullOrEmpty(args[0])) ? args[0] : "Game";
        
        IntPtr hwnd = CreateWindowEx(
            WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE,
            "STATIC",
            title,
            WS_POPUP,
            -10000, -10000, 10, 10,
            IntPtr.Zero, IntPtr.Zero, IntPtr.Zero, IntPtr.Zero
        );

        if (hwnd != IntPtr.Zero) {
            ShowWindow(hwnd, SW_SHOWNA);
        }

        MSG msg;
        while (GetMessage(out msg, IntPtr.Zero, 0, 0)) {
            TranslateMessage(ref msg);
            DispatchMessage(ref msg);
        }
    }
}
