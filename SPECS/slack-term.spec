%define debug_package %{nil}

%global gh_user     erroneousboat
%global gh_commit   2ee21247add4e50660e8b3b90b285814d21d8ad6
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})

# see https://fedoraproject.org/wiki/PackagingDrafts/Go#Build_ID
%global _dwz_low_mem_die_limit 0
%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') " -i -v -x %{?**};
%endif

Name:           slack-term
Version:        0.5.0
Release:        1%{?dist}
Summary:        Slack client for your terminal
Group:          Applications/System
License:        MIT
URL:            https://github.com/%{gh_user}/%{name}
BuildRequires:  git golang

%description
A Slack client for your terminal.

%prep
wget https://github.com/%{gh_user}/%{name}/archive/v%{version}.tar.gz
tar xzf v%{version}.tar.gz
mkdir -p %{_builddir}/src/github.com/%{gh_user}/
cd %{_builddir}/src/github.com/%{gh_user}/
ln -snf %{_builddir}/%{name}-%{version} %{name}
cd %{name}

%build
export GOPATH="%{_builddir}"
export PATH=$PATH:"%{_builddir}"/bin
cd %{_builddir}/src/github.com/%{gh_user}/%{name}
export LDFLAGS="${LDFLAGS} -X main.commit=%{gh_short} -X main.date=$(date -u +%Y%m%d.%H%M%%S) -X main.version=%{version}"

%gobuild -o %{_builddir}/bin/%{name}

%install
install -Dm0755 %{_builddir}/bin/%{name} %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%doc %{name}-%{version}/LICENSE %{name}-%{version}/*.md

%changelog
* Mon Mar 16 2020 Jamie Curnow <jc@jc21.com> 0.5.0-1
- v0.5.0

* Fri Mar 22 2019 Jamie Curnow <jc@jc21.com> 0.4.1-1
- v0.4.1

