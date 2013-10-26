#!/usr/local/bin/perl
#
# Copyright (c) 2006 Jiro Nishiguchi <jiro@cpan.org>
# All rights reserved.
use strict;
use warnings;

use CGI;
use YAML ();
use Template;
use Yahoo::BBAuth;
use XML::Simple ();

my $q = CGI->new;
if ($q->param('src')) {
    show_myself();
}
my $config = YAML::LoadFile('/tmp/bbauth.yaml');
my $api = Yahoo::BBAuth->new(
    appid  => $config->{appid},
    secret => $config->{secret},
);
my $param = { q => $q };
unless ($q->param('token')) {
    $param->{auth_url} = $api->auth_url;
} else {
    if ($api->validate_sig) {
        my $xml = $api->auth_ws_get_call('http://photos.yahooapis.com/V3.0/listAlbums');
        if ($xml) {
            my $result = XML::Simple::XMLin($xml, ForceArray => ['Album']);
            $param->{result} = $result;
        } else {
            $param->{error} = $api->access_credentials_error;
        }
    } else {
        $param->{error} = $api->sig_validation_error;
    }
}
my $tt = Template->new;
print $q->header(-charset => 'utf-8');
$tt->process(\*DATA, $param) or die $tt->error;

sub show_myself {
    print $q->header('text/plain; charset=utf-8');
    open 0 and print <0>;
    exit;
}

__END__
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Your Yahoo! Photos Albums</title>
</head>
<body>
<div><a href="./?src=1">cgi source</a>, <a href="http://search.cpan.org/dist/Yahoo-BBAuth/">module source</a></div>
<div>
<h1>Test BBauth With Yahoo! Photos</h1>
<div>
[% IF auth_url %]
You have not authorized access to your Yahoo! Photos account yet<br /><br />
<a href="[% auth_url %]">Click here to authorize</a>
[% ELSIF error %]
[% error %]
[% ELSE %]
<h2>BBauth authentication Successful</h2>
[% album_num %]
[% FOREACH album = result.Album %]
[% IF album.Image.content %][% album_num = album_num + 1 %]<img src="[% album.Image.content %]" /><br />[% END %]
[% END %]
[% UNLESS album_num %]no album..[% END %]
[% END %]
</div>
</div>
</body>
</html>
