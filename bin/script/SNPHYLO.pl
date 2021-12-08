#!/usr/bin/perl

#####
#	Command
#	#./SNPHYLO.pl -p [parameter file] -o [out directory]
#
#	Input
#	Merged hapmap file
#
#	Output
#	Newick tree
#
#	Information
#	Made by Jongin
#	2018.08.27
#   Update by NY
#   2021. 01.
#####

use strict;
use warnings;
use Getopt::Long qw(:config no_ignore_case);
use File::Basename;
use FindBin qw($Bin);
use Cwd 'abs_path';
use Switch;

## Parameters
my $param_f;
my $outdir = "./",
my $help = 0;

GetOptions (
	"param|p=s"	=>	\$param_f,
	"outdir|o=s"	=>	\$outdir,
	"help|h"		=> 	\$help,
);

$outdir = abs_path($outdir);
`mkdir -p $outdir`;

if ($help == 1 || !$param_f) {
	print STDERR "usage:\n\$./SNPHYLO.pl -H HAPMAP_FILE -s SAMPLE_NUMBER -o OUR_DIR\n\n";
	print STDERR "optional arguments:\n";
	print STDERR "\t-h, --help\tshow this help message and exit\n";
	print STDERR "\t-p, --param\tPARAM\n\t\t\t\t<Path> parameter file\n";
	print STDERR "\t-o, --outdir\tOUT_DIR\n\t\t\t\t<Path> Output directory\n";
	print STDERR "\n================================================\n\n";
	exit;
}

### Configure parameters
my $snphylo_cmd = "";
my $dendogram = $Bin."/visTREE.R";
my $hapmapfilt = $Bin."/HAPMAP_FILT.pl";
my $hapmap_f = "";
my $sampleNum = 0;

open(PARAM, $param_f);
while(<PARAM>){
	chomp;
	if($_ =~ /^#/ || $_ eq ""){next;}
	my @p = split(/\s*=\s*/,$_);
	switch ($p[0]) {
		case("Snphylo"){$snphylo_cmd = abs_path($p[1]);}
		case("hapmap"){$hapmap_f = abs_path($p[1]);}
		case("sampleNum"){$sampleNum = $p[1];}
	}
}
close(PARAM);

$hapmap_f = abs_path($hapmap_f);
chdir($outdir);
print STDERR "$hapmapfilt $hapmap_f > $outdir/filtered.hapmap\n";
print STDERR "$snphylo_cmd -H $hapmap_f -P snphylo -A -b >& $outdir/snphylo.log\n";
print STDERR "$dendogram $outdir/snphylo.ml.tree $sampleNum ./\n";

my $output = `$hapmapfilt $hapmap_f > $outdir/filtered.hapmap`;
if($?) {
    exit $? >> 8;
}

$hapmap_f = abs_path("$outdir/filtered.hapmap");

$output = `$snphylo_cmd -H $hapmap_f -P snphylo -A -b`;
if($?) {
	exit $? >> 8;
}

$output = `$dendogram $outdir/snphylo.ml.tree  $sampleNum  $outdir`;
if($?) {
	exit $? >> 8;
}
