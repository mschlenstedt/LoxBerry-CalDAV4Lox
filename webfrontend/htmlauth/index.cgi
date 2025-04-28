#!/usr/bin/perl

# This is a sample Script file
# It does not much:
#   * Loading configuration
#   * including header.htmlfooter.html
#   * and showing a message to the user.
# That's all.

use LoxBerry::Web;
use LoxBerry::Log;
use CGI qw/:standard/;
use warnings;
use strict;
no strict "refs"; # we need it for template system
use URI::Encode qw(uri_decode);

my  $cfg;
my  $conf;
our $selecteddepth0 = "";
our $selecteddepth1 = "";
our $selecteddownhelper0 = "";
our $selecteddownhelper1 = "";
our $selectedhttpauth0 = "";
our $selectedhttpauth1 = "";
our $selectedhttpauth2 = "";
our $selectedhttpauth3 = "";
our $selectedhttpauth4 = "";
our $selectedhttpauth5 = "";
our $selectedhttpauth6 = "";
our $selectedhttpauth7 = "";
our $selectedhttpauth8 = "";
our $selectedhttpauth9 = "";
my  $curl;
our $depth;
our $caldavurl;
our $caldavuser;
our $caldavpass;
our $httpauth;
our $bearer;
our $downhelper;
our $fwdays;
our $delay;
our $events;
our $dotest;
our $helptext;
our $helplink;
our $helptemplate;
our $template_title;
our $namef;
our $value;
our %query;
our $do;
our $cache;

my $log = LoxBerry::Log->new (
        name => 'caldav4lox',
        filename => "$lbplogdir/caldav4lox.log",
        append => 1,
        addtime => 1
);
LOGSTART "CalDAV-4-Lox configuration helper";

LOGDEB "Read system settings";
# Read Settings
$cfg             = new Config::Simple("$lbsconfigdir/general.cfg");
$curl            = $cfg->param("BINARIES.CURL");
LOGDEB "Done";

LOGDEB "retrieve values from URL";
# Everything from URL
foreach (split(/&/,$ENV{'QUERY_STRING'}))
{
  ($namef,$value) = split(/=/,$_,2);
  $namef =~ tr/+/ /;
  $namef =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $query{$namef} = $value;
}

# Set parameters coming in - get over post
	if ( !$query{'do'} )           { if ( param('do')           ) { $do           = quotemeta(param('do'));           } else { $do           = "form"; } } else { $do           = quotemeta($query{'do'});           }
	if ( !$query{'caldavurl'} )    { if ( param('caldavurl')    ) { $caldavurl    = param('caldavurl');               } else { $caldavurl    = "";     } } else { $caldavurl    = $query{'caldavurl'};               }
	if ( !$query{'caldavuser'} )   { if ( param('caldavuser')   ) { $caldavuser   = param('caldavuser');              } else { $caldavuser   = "";     } } else { $caldavuser   = $query{'caldavuser'};              }
	if ( !$query{'caldavpass'} )   { if ( param('caldavpass')   ) { $caldavpass   = param('caldavpass');              } else { $caldavpass   = "";     } } else { $caldavpass   = $query{'caldavpass'};              }
	if ( !$query{'httpauth'} )     { if ( param('httpauth')     ) { $httpauth     = param('httpauth');                } else { $httpauth     = "";     } } else { $httpauth     = $query{'httpauth'};                }
	if ( !$query{'bearer'} )       { if ( param('bearer')       ) { $bearer       = param('bearer');                  } else { $bearer       = "";     } } else { $bearer       = $query{'bearer'};                  }
	if ( !$query{'downhelper'} )   { if ( param('downhelper')   ) { $downhelper   = param('downhelper');              } else { $downhelper   = "";     } } else { $downhelper   = $query{'downhelper'};            }
	if ( !$query{'fwdays'} )       { if ( param('fwdays')       ) { $fwdays       = param('fwdays');                  } else { $fwdays       = "";     } } else { $fwdays       = $query{'fwdays'};                  }
	if ( !$query{'delay'} )        { if ( param('delay')        ) { $delay        = param('delay');                   } else { $delay        = "";     } } else { $delay        = $query{'delay'};                   }
	if ( !$query{'events'} )       { if ( param('events')       ) { $events       = param('events');                  } else { $events       = "";     } } else { $events       = $query{'events'};                  }
	if ( !$query{'dotest'} )       { if ( param('dotest')       ) { $dotest       = param('dotest');                  } else { $dotest       = "";     } } else { $dotest       = $query{'dotest'};                  }
	if ( !$query{'cache'} )        { if ( param('cache')        ) { $cache        = param('cache');                   } else { $cache        = "";     } } else { $cache        = $query{'cache'};                   }
LOGDEB "Done";

LOGDEB "read CalDAV-4-Lox settings";
# read caldav4lox configs
$conf = new Config::Simple("$lbpconfigdir/caldav4lox.conf");
$depth = $conf->param('general.Depth');
LOGDEB "Done";
if ( $depth == 0 ) {$selecteddepth0="selected"} else { $selecteddepth1="selected"}
if ( $downhelper == 0 ) {$selecteddownhelper0="selected"} else { $selecteddownhelper1="selected"}
if ( $httpauth eq "ANY" ) {$selectedhttpauth0="selected"};
if ( $httpauth eq "ANYSAFE" ) {$selectedhttpauth1="selected"};
if ( $httpauth eq "BASIC" ) {$selectedhttpauth2="selected"};
if ( $httpauth eq "DIGEST" ) {$selectedhttpauth3="selected"};
if ( $httpauth eq "DIGEST_IE" ) {$selectedhttpauth4="selected"};
if ( $httpauth eq "BEARER" ) {$selectedhttpauth5="selected"};
if ( $httpauth eq "NEGOTIATE" ) {$selectedhttpauth6="selected"};
if ( $httpauth eq "NTLM" ) {$selectedhttpauth7="selected"};
if ( $httpauth eq "NTLM_WB" ) {$selectedhttpauth8="selected"};
if ( $httpauth eq "ONLY" ) {$selectedhttpauth9="selected"};

LOGDEB "retrieve the local ip";
require IO::Socket::INET;
my $localip = LoxBerry::System::get_localip();
my $localPort = "";
if ( LoxBerry::System::lbwebserverport() != 80) { $localPort = ":".LoxBerry::System::lbwebserverport() }
LOGDEB "localIP: $localip$localPort";
LOGDEB "Done";

LOGDEB "retrieve the defaul gateway";
my $gw = `netstat -nr`;
$gw =~ m/0.0.0.0\s+([0-9]+.[0-9]+.[0-9]+.[0-9]+)/g;
my $gwip = $1;
LOGDEB "gateway: $gwip";
LOGDEB "Done";

LOGDEB "create the page - beginn";
# Title
$template_title = "CalDAV-4-Lox";
# Create help page
$helplink = "https://wiki.loxberry.de/plugins/caldav_4_lox/start";
$helptemplate = "help.html";
LOGDEB "print out the header";
LoxBerry::Web::lbheader(undef,$helplink,$helptemplate);

LOGDEB "create the content";
# Load content from template
my $maintemplate = HTML::Template->new(
    filename => "$lbptemplatedir/content.html",
    global_vars => 1,
    loop_context_vars => 1,
    die_on_bad_params => 0,
);
$maintemplate->param("psubfolder",$lbpplugindir);
$maintemplate->param("selecteddepth0", $selecteddepth0);
$maintemplate->param("selecteddepth1", $selecteddepth1);
$maintemplate->param("selectedhttpauth0", $selectedhttpauth0);
$maintemplate->param("selectedhttpauth1", $selectedhttpauth1);
$maintemplate->param("selectedhttpauth2", $selectedhttpauth2);
$maintemplate->param("selectedhttpauth3", $selectedhttpauth3);
$maintemplate->param("selectedhttpauth4", $selectedhttpauth4);
$maintemplate->param("selectedhttpauth5", $selectedhttpauth5);
$maintemplate->param("selectedhttpauth6", $selectedhttpauth6);
$maintemplate->param("selectedhttpauth7", $selectedhttpauth7);
$maintemplate->param("selectedhttpauth8", $selectedhttpauth8);
$maintemplate->param("selectedhttpauth9", $selectedhttpauth9);
$maintemplate->param("selecteddownhelper0", $selecteddownhelper0);
$maintemplate->param("selecteddownhelper1", $selecteddownhelper1);
$maintemplate->param("lang",lblanguage());
$maintemplate->param("caldavurl",$caldavurl);
$maintemplate->param("caldavuser",$caldavuser);
$maintemplate->param("caldavpass",$caldavpass);
$maintemplate->param("httpauth",$httpauth);
$maintemplate->param("bearer",$bearer);
$maintemplate->param("downhelper",$downhelper);
$maintemplate->param("fwdays",$fwdays);
$maintemplate->param("delay",$delay);
$maintemplate->param("cache",$cache);
$maintemplate->param("events",$events);
$maintemplate->param("logdir",$lbplogdir);

%L = LoxBerry::System::readlanguage($maintemplate, "language.ini");
  
print $maintemplate->output;

if ( $caldavurl =~ m{
    (
        (ftp|https?):\/\/
        ([a-z0-9\-_]+(:[^@]+)?\@)?
        (
            ([a-z0-9\.\-]+)\.([a-z\.]{2,6})
            |
            ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})
        )
        (:[0-9]{2,5})?
        (
            [a-z0-9\.\-_/\+\%&;\:,\=\!@\(\)\[\]~\'\"]*
            [a-z0-9\.\-_/\+\%&;\:,\=\!@\(\)\[\]~]+
        )
        (\?[a-z0-9\.\-_/\+\%&;\:,\=\!@\(\)\[\]~]*)?
        (\#[a-z0-9\.\-_/\+\%&;\:,\=\!@\(\)\[\]~]*)?
    )
}gisx) {
	LOGINF "URL was given, generate answer";
	my $tempcalurl = $caldavurl; 
	$tempcalurl =~ s/\:/\%3A/g;
	my $tempevents = $events;
	$tempevents =~ s/\n/\|/g;
	$tempevents =~ s/\r//g;
	$tempevents =~ s/ //g;
	my $tempURL = "http://$localip$localPort/plugins/$lbpplugindir/caldav.php?calURL=$tempcalurl&user=$caldavuser&pass=$caldavpass";
	if ( $fwdays ) { if (($fwdays > 0) && ($fwdays < 364)) {$tempURL .= "&fwdays=$fwdays";}}
	if ( $delay ) { if (($delay > 0) && ($fwdays < 1440)) {$tempURL.= "&delay=$delay";}}
	if ( $cache ) { if (($cache > 0) && ($cache < 1440)) {$tempURL.= "&cache=$cache";}}
	if ( $httpauth ) { $tempURL.= "&httpauth=$httpauth";}
	if ( $bearer && $httpauth ) { $tempURL.= ":$bearer";}
	if ( $downhelper ) { $tempURL.= "&downhelper=$downhelper";}
	$tempURL .= "&events=$tempevents";
	print "<p>". $L{"LABEL.TXT0006"} . ": <a href=$tempURL target='_blank'>$tempURL</a></p>\n";
	LOGDEB "test the calendar";
	my $test = `$curl '$tempURL'`;
	if ($test eq "") {LOGERR "no answer from curl";}
	if ($test =~ m{HTTP/[0-9]\.[0-9][ ]?([4-5][0-9][0-9])}) {
		LOGERR "calendar returns an error";
		LOGDEB "$test";
		$test = "";	
	}
	print "<p><pre class=\"textfield\">$test</pre></p>";
	LOGDEB "Done";
	print "<p>" . $L{"LABEL.TXT0000"} . ":\n";
	if ($tempevents eq "") {print "<p></p>\n";}
	foreach (split(/\|/,$tempevents))
	{
		if ($_ ne "*") {
			my $uri = URI::Encode->new({encode_reserved => 0});
			my $en = $uri->decode($_);
			my @en = split (/@@/, $en);
			print "<p>$en[0]:</ br><ul style=\"display: table;\">\n<li style=\"display: table-row;\"><div style=\"width: 15%; display: table-cell;\">" . $L{"LABEL.TXT0001"} . "</div>: <span style=\"background-color: #cccccc\">$en[0]\": {\\i\"Start\"\\i: \\v</span></li>\n<li style=\"display: table-row;\"><div style=\"width: 15%; display: table-cell;\">" . $L{"LABEL.TXT0002"} . "</div>: <span style=\"background-color: #cccccc\">$en[0]\": {\\i\"End\"\\i: \\v</span></li>\n<li style=\"display: table-row;\"><div style=\"width: 15%; display: table-cell;\">" . $L{"LABEL.TXT0003"} . "</div>: <span style=\"background-color: #cccccc\">$en[0]\": {\\i\"fwDay\"\\i: \\v</span></li>\n<li style=\"display: table-row;\"><div style=\"width: 15%; display: table-cell;\">" . $L{"LABEL.TXT0004"} . "</div>: <span style=\"background-color: #cccccc\">$en[0]\": {\\i\"wkDay\"\\i: \\v</span></li>\n</ul></p>";
		}
	}
	print $L{"LABEL.TXT0005"} . ": <span style=\"background-color: #cccccc\">\"now\": \\v</span></p>\n";
}

LOGDEB "print out the footer";
# Load footer and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
LoxBerry::Web::lbfooter();
LOGEND "Done";

exit;
