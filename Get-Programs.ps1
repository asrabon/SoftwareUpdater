$programs = "Name*Version*Publisher*UninstallString*InstallDate`n"
#Open Remote Base
$reg=[microsoft.win32.registrykey]::OpenRemoteBaseKey('LocalMachine',$Computer)

#Check if it's got 64bit regkeys
$keyRootSoftware = $reg.OpenSubKey("SOFTWARE")
[bool]$is64 = ($keyRootSoftware.GetSubKeyNames() | ? {$_ -eq 'WOW6432Node'} | Measure-Object).Count
$keyRootSoftware.Close()

#Get all of they keys into a list
$softwareKeys = @()
if ($is64){
    $pathUninstall64 = "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    $keyUninstall64 = $reg.OpenSubKey($pathUninstall64)
    $keyUninstall64.GetSubKeyNames() | % {
        $softwareKeys += $pathUninstall64 + "\\" + $_
    }
    $keyUninstall64.Close()
}
$pathUninstall32 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
$keyUninstall32 = $reg.OpenSubKey($pathUninstall32)
$keyUninstall32.GetSubKeyNames() | % {
    $softwareKeys += $pathUninstall32 + "\\" + $_
}
$keyUninstall32.Close()

#Get information from all the keys
$softwareKeys | % {
    $subkey=$reg.OpenSubKey($_)
    if ($subkey.GetValue("DisplayName")){
        $installDate = $null
        if ($subkey.GetValue("InstallDate") -match "/"){
            $installDate = Get-Date $subkey.GetValue("InstallDate")
        }
        elseif ($subkey.GetValue("InstallDate").length -eq 8){
            $installDate = Get-Date $subkey.GetValue("InstallDate").Insert(6,".").Insert(4,".")
        }
        $programs = $programs + $subkey.GetValue("DisplayName") + "*" + $subKey.GetValue("DisplayVersion") + "*" + $subkey.GetValue("Publisher") + "*" + $subkey.GetValue("UninstallString") + "*" + $installDate + "`n"
    }

    $subkey.Close()
}
Write-Host $programs
$reg.Close()