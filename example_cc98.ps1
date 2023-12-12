while ($true)
{
    $ComputerName = ''
    $IPv4 = [System.Net.Dns]::GetHostAddresses($ComputerName) |
    Where-Object {
    $_.AddressFamily -eq 'InterNetwork'
    } |
    Select-Object -ExpandProperty IPAddressToString |
    Out-String

    $IPv6obj = [System.Net.Dns]::GetHostAddresses($ComputerName) |
    Where-Object {
    $_.AddressFamily -eq 'InterNetworkV6'
    } |
    Select-Object -ExpandProperty IPAddressToString

    $IPv6 = ""
    foreach ($i in $IPv6obj)
    {
        if ($i.Substring(0,4) -ne "fe80") 
        {
            $IPv6 += $i + "`n"
        }
    }
	
    $From = "xxx@zju.edu.cn" #发送邮箱地址，改成你的邮箱地址
    $To = "xxx@zju.edu.cn" #发给自己比较方便，推荐改成你的邮箱地址
    $Subject = "IP" #邮件主题，可以方便合并整理，避免刷屏
    if ([String]::IsNullOrEmpty($Body) -or $Body -ne $IPv4 + $IPv6) 
    {
        $Body = $IPv4 + $IPv6
        $smtpServer = "smtp.zju.edu.cn" #浙大邮箱无需连接外网即可使用，当然你也可换成其他邮箱的smtp服务器
        $smtpPort = 25
        $username = "您的邮箱账户如318010XXXX" #改成你的邮箱账户名，注意这里应该填入的是@zju.edu.cn之前的内容，即仅填写你的学号即可
        $password = "您的邮箱密码" #改成你的邮箱密码
        $SMTPMessage = New-Object System.Net.Mail.MailMessage($From, $To, $Subject, $Body)
        $SMTPClient = New-Object Net.Mail.SmtpClient($smtpServer, $SmtpPort) 
        $SMTPClient.EnableSsl = $false 
        $SMTPClient.Credentials = New-Object System.Net.NetworkCredential($username, $password); 
        $SMTPClient.Send($SMTPMessage)
        Write-Output "IP changed,e-mail has been send"
        Start-Sleep -Seconds 15
        continue
    }
    Start-Sleep -Seconds 15 #延时15秒
    Write-Output "IP not changed" 
}