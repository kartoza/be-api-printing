# Standalone install

## Instructions to Run a Node.js App on IIS Server

### Step 1: Install IIS on Windows
1. Open **Control Panel**.
2. Navigate to **Programs** > **Turn Windows features on or off**.
3. Scroll down and check the box for **Internet Information Services (IIS)**.
4. Expand the IIS tree and ensure the following components are selected:
   - **Web Management Tools**
   - **World Wide Web Services**
   - **Application Development Features** (ensure CGI and ISAPI Extensions are checked)
5. Click **OK** and wait for IIS to install.

### Step 2: Install URL Rewrite Module
- Download and install the **IIS URL Rewrite Module** from the Microsoft website. This module allows IIS to act as a reverse proxy, forwarding requests to your Node.js app.

### Step 3: Install IISNode
- Download **iisnode** from the iisnode GitHub releases page.
- Install it on your machine. IISNode allows you to host Node.js applications in IIS.

### Step 4: Configure IIS to Host the Node.js App
1. Open **IIS Manager** (type `inetmgr` in the Start menu search).
2. Right-click **Sites** and choose **Add Website**.
3. Set the **Site name**, the **Physical path** (the folder where your Node.js app is located), and choose a **Port** (e.g., 8080).
4. Click **OK**.

### Step 5: Configure URL Rewrite for Reverse Proxy
1. In **IIS Manager**, select your site, then double-click on the **URL Rewrite** option.
2. Click **Add Rule(s)** in the Actions pane on the right, then choose **Reverse Proxy**.
3. If prompted, enable **Application Request Routing (ARR)** by clicking on the prompt at the top of the window and checking the box.
4. In the **Reverse Proxy Rules** dialog, enter the Node.js app's hostname and port (e.g., `localhost:3000`).
5. Click **Apply**.

### Step 6: Configure web.config
In the root of your Node.js application directory, create a `web.config` file with the following content:

```xml
<configuration>
  <system.webServer>
    <handlers>
      <add name="iisnode" path="server.js" verb="*" modules="iisnode" />
    </handlers>
    <rewrite>
      <rules>
        <rule name="Node.js app">
          <match url="/*" />
          <action type="Rewrite" url="server.js" />
        </rule>
      </rules>
    </rewrite>
    <iisnode 
      devErrorsEnabled="true"
      loggingEnabled="true"
      debuggingEnabled="true" 
      maxNamedPipeConnectionRetry="10"
      gracefulShutdownTimeout="3000" />
    <httpErrors errorMode="Detailed">
      <remove statusCode="404" />
      <remove statusCode="500" />
      <error statusCode="404" path="/404.html" responseMode="ExecuteURL" />
      <error statusCode="500" path="/500.html" responseMode="ExecuteURL" />
    </httpErrors>
  </system.webServer>
</configuration>
```

### Step 7
*Grant Permissions*
- Navigate to your application's directory in the file system.
- Right-click the folder, select Properties, and go to the Security tab.
- Add the application pool identity (e.g., IIS AppPool\DefaultAppPool) and grant Read & Execute and Write permissions.

# Sending request

- Url: `/print`
- Method: `POST`
- Body :
```
{
    "url": []
}
```

