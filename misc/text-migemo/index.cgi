#!/usr/local/bin/perl
# $Id$
# Copyright (c) 2006 Jiro Nishiguchi <jiro@cpan.org>
# All rights reserved.
use strict;
use warnings;
use utf8;
use open ':encoding(utf-8)';

use CGI qw(:standard);
use Encode;
use Template;
use Text::Migemo;

binmode STDOUT, ':encoding(utf-8)';

my @prefs = qw(
    北海道 青森県 岩手県 宮城県 秋田県 山形県 福島県 茨城県 栃木県 群馬県
    埼玉県 千葉県 東京都 神奈川県 新潟県 富山県 石川県 福井県 山梨県 長野県
    岐阜県 静岡県 愛知県 三重県 滋賀県 京都府 大阪府 兵庫県 奈良県 和歌山県
    鳥取県 島根県 岡山県 広島県 山口県 徳島県 香川県 愛媛県 高知県 福岡県
    佐賀県 長崎県 熊本県 大分県 宮崎県 鹿児島県 沖縄県
);

my $q = CGI->new;
if ($q->param('src')) {
    show_myself();
}
if ($q->request_method eq 'GET') {
    my $tt = Template->new;
    $tt->process(\*DATA, { q => $q, prefs => \@prefs }, \my $output);
    print $q->header(-charset => 'utf-8');
    print $output;
    exit;
}
my $migemo = Text::Migemo->new("/usr/local/share/migemo/euc-jp/migemo-dict");
my $query = $q->param('q');
my @list;
if ($query) {
    my $result = $migemo->query(quotemeta $query);
    $result = decode('euc-jp', $result);
    my $re = qr/^$result/;
    for my $pref (@prefs) {
        push @list, $pref if $pref =~ $re;
    }
} else {
    @list = @prefs;
}
print $q->header(-charset => 'utf-8');
print ul(map { li($_) } @list);

sub show_myself {
    print $q->header('text/plain; charset=utf-8');
    open 0 and print <0>;
    exit;
}

__END__
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="ja" xml:lang="ja" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<link rel="index" href="/" />
<link rev="made" href="mailto:spiritloose&#64;gmail.com" />
<link rel="stylesheet" href="/css/style.css" type="text/css" />
<title>Text::Migemo Demo</title>
<script type="text/javascript" src="/js/prototype.js"></script>
<script type="text/javascript">
<!--
Event.observe(window, 'load', function() {
    Form.focusFirstElement('search');
    new Form.Element.Observer('q', 0.5, search);
    Event.observe('search', 'submit', search);

});
function search() {
    Element.show('loading');
    new Ajax.Updater('result', './index.cgi', {
        onComplete: function(request) {
            Element.hide('loading');
        },
        parameters: Form.serialize('search')
    });
    return false;
}
// -->
</script>
</head>
<body>
<div class="wrapper"><div id="container">
<div id="header"><a href="[% q.script_name %]?src=1">source</a> | <a href="http://d.hatena.ne.jp/spiritloose/20060824/1156376878">About</a> | <a href="/">Home</a></div>
<div id="content">
<h1><a href="http://search.cpan.org/dist/Text-Migemo/">Text::Migemo</a> Demo</h1>
<p>
<form id="search" action="./">
都道府県をローマ字で入力<br />
<input type="text" id="q" name="q" value="" tabindex="1" accesskey="s" autocomplete="off" style="ime-mode: disabled;" />
<span id="loading" style="display: none;"><img src="./loading.gif" /></span>
</form>
</p>
<div id="result">
<ul>
[% FOR pref = prefs %]
<li>[% pref %]</li>
[% END %]
</ul>
</div>
</div>
<div id="footer">
<address>&#169; 2006 <a href="http://spiritloose.net/">Jiro Nishiguchi</a>.</address>
<img src="/img/mailto.png" width="159" height="21" alt="mail address" />
</div>
</div></div>
</body>
</html>
