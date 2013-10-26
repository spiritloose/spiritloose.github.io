#!/usr/local/bin/perl
#
# Copyright (c) 2006 Jiro Nishiguchi <jiro@cpan.org>
# All rights reserved.
use strict;
use warnings;

use CGI;
use Encode;
use Template;
use HTML::FillInForm;
use Geo::Coder::Ja qw(:all);

my $q = CGI->new;
show_myself() if $q->path_info eq '/src';
print $q->header(-charset => 'utf-8');
my $tt = Template->new;
my $param = { q => $q };
if (my $location = $q->param('q')) {
    my $geocoder = Geo::Coder::Ja->new(
        dbpath     => '/usr/local/share/geocoderja',
        load_level => DB_CHO,
        encoding   => 'UTF-8',
    );
    $param->{result} = $location =~ /^\d{7}$/ ? $geocoder->geocode(postcode => $location)
            : $geocoder->geocode(location => $location);
    $tt->process(\*DATA, $param, \my $output);
    $output = decode('utf8', $output);
    $output = HTML::FillInForm->new->fill(scalarref => \$output, fobject => $q);
    print encode('utf8', $output);
} else {
    $tt->process(\*DATA, $param);
}

sub show_myself {
    open FH, $0 or die;
    print $q->header(-type => 'text/plain', -charset => 'utf-8');
    print <FH>;
    close FH;
    exit;
}

__END__
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="ja" xml:lang="ja" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<link rel="index" href="./" />
<link rev="made" href="mailto:spiritloose&#64;gmail.com" />
<link rel="stylesheet" href="/css/style.css" type="text/css" />
<script type="text/javascript" src="/js/prototype.js"></script>
<script type="text/javascript">
//<![CDATA[
Event.observe(window, 'load', function(){
    Form.focusFirstElement('search');
});
//]]>
</script>
<title>Geo::Coder::Ja Demo</title>
</head>
<body>
<div class="wrapper"><div id="container">
<div id="header">
<a href="[% q.script_name %]/src">source</a> | <a href="http://d.hatena.ne.jp/spiritloose/20061120/1163983849">About</a> | <a href="/">Home</a>
</div>
<div id="content">
<h1><a href="http://search.cpan.org/dist/Geo-Coder-Ja/">Geo::Coder::Ja</a> Demo</h1>
<p>デモのため、行政区域までしか検索できません。</p>
<form id="search" action="./">
<p>
住所または郵便番号:(例:東京都渋谷区/1500002)<br />
<input type="text" size="40" name="q" />
<input type="submit" value="検索" />
</p>
</form>
[% IF result %]
<p>
[% USE gmap = url('http://maps.google.com/maps') %]
[% ll = result.latitude _ ',' _ result.longitude %]
<a href="[% gmap(q => result.address, ie => 'UTF8', ll => ll) %]">Google Maps</a><br />
緯度：[% result.latitude %]<br />
経度：[% result.longitude %]<br />
住所：[% result.address %]<br />
住所(かな)：[% result.address_kana %]
</p>
[% END %]
</div>
<div id="footer">
<address>&#169; 2006 <a href="http://spiritloose.net/">Jiro Nishiguchi</a>.</address>
<img src="/img/mailto.png" width="159" height="21" alt="mail address" />
</div>
</div></div>
</body>
</html>
