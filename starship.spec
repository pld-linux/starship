%define		crates_ver	1.25.1

Summary:	The minimal, blazing-fast, and infinitely customizable cross-shell prompt
Name:		starship
Version:	1.25.1
Release:	1
License:	ISC
Group:		Applications/Shells
Source0:	https://github.com/starship/starship/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bb8175f295eb734cad5c26fddc2a5eea
# cd starship-%{version}
# cargo vendor
# cd ..
# tar cJf starship-crates-%{version}.tar.xz starship-%{version}/{vendor,Cargo.lock}
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	ca10f1e32ae9968b2387b3b4b09cc6c7
URL:		https://starship.rs/
BuildRequires:	cargo
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust >= 1.90
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?rust_req}
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Starship is the minimal, blazing-fast, and infinitely customizable
prompt for any shell. Shows the information you need, while staying
sleek and minimal. Quick installation available for Bash, Fish, ZSH,
Ion, Tcsh, Elvish, Nu, Xonsh, Cmd and PowerShell.

%package -n bash-completion-starship
Summary:	Bash completion for starship
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-starship
Bash completion for starship.

%package -n fish-completion-starship
Summary:	fish-completion for starship
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-starship
fish-completion for starship.

%package -n zsh-completion-starship
Summary:	Zsh completion for starship
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-starship
Zsh completion for starship.

%prep
%setup -q -a1

%{__mv} %{name}-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

install -d $RPM_BUILD_ROOT{%{bash_compdir},%{fish_compdir},%{zsh_compdir}}

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD
%{cargo_objdir}/starship completions bash > $RPM_BUILD_ROOT%{bash_compdir}/starship
%{cargo_objdir}/starship completions fish > $RPM_BUILD_ROOT%{fish_compdir}/starship.fish
%{cargo_objdir}/starship completions zsh  > $RPM_BUILD_ROOT%{zsh_compdir}/_starship

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md LICENSE README.md SECURITY.md
%attr(755,root,root) %{_bindir}/starship

%files -n bash-completion-starship
%defattr(644,root,root,755)
%{bash_compdir}/starship

%files -n fish-completion-starship
%defattr(644,root,root,755)
%{fish_compdir}/starship.fish

%files -n zsh-completion-starship
%defattr(644,root,root,755)
%{zsh_compdir}/_starship
