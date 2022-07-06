# Eduroam WiFi Authentication Instructions

Ask for assistance from a professor or a more experienced peer to help you if these instructions are not clear.

## Version

The instructions are valid as of Summer 2022.

## CSUF IT Wizard (recommended)

CSUF's IT provides an online wizard for configuring Eduroam to download an executable to install the eduroam wireless profile and CA Certificate.

The Online Wizard can be found at http://wireless.fullerton.edu/eduroam.php. Follow the steps provided to download and run the `SecureW2_JoinNow.run` executable to configure the eduroam wireless profile.

## Manual Configuration (not recommended)

Adding the Eduroam profile manually uses an inherently less secure method of authentication. If possible, the CSUF IT Wizard instructions above should be followed.

Make sure you type your username and password very carefully in the last two steps. This will save you time and avoid having something that looks right but it is broken.
1. Go to the WiFi menu and choose 'Select Network'
1. Select 'eduroam'; you may have to wait a minute for it to appear or select 'more networks' to see 'eduroam'. A window will appear where you can enter security and login information for eduroam.
1. Look for the drop down menu labeled 'Authentication'. Change the value to 'Protected EAP (PEAP)'.
1. Look for the checkbox that is labeled 'No CA certificate is required'. Check this box.
1. Look for the drop down menu labeled 'Inner Authentication'. Make sure it is set to 'MSCHAPv2'.
1. Look for the text box labeled 'Username'. In this text box enter your CSUF email address. For example, your email address looks like 'kai@csu.fullerton.edu'.
1. Look for the text box labeled 'Password'. In this text box enter your CSUF portal password. **Make sure you type this password correctly. Please click 'Show Password' and verify your password.**
1. The WiFi menu will refresh after a few minutes to show that you are connected to a network. Open your web browser and load up a web page such as http://www.fullerton.edu.
