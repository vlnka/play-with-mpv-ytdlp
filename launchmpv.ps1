# change path
$mpvPath = "D:\Programs\mpv\mpv.exe"
$mpvProcess = Get-Process -Name "mpv" -ErrorAction SilentlyContinue

if ($mpvProcess -eq $null) {
    $mpvArg = $args[0]

    if ($mpvArg -eq $null) {
        Write-Host "Please provide an argument for 'mpv.exe'."
    } else {
        $mpvProcess = Start-Process -FilePath $mpvPath -ArgumentList $mpvArg -PassThru -WindowStyle Hidden
        $mpvProcess.WaitForInputIdle()
        Add-Type -AssemblyName PresentationFramework
        [System.Windows.Application]::Current.Windows
    }
} else {
    Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;

        public class WindowHelper {
            [DllImport("user32.dll")]
            [return: MarshalAs(UnmanagedType.Bool)]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
        }
"@
    [WindowHelper]::SetForegroundWindow($mpvProcess.MainWindowHandle)   
    Write-Host "mpv.exe is already running. New instances are not allowed."
}
