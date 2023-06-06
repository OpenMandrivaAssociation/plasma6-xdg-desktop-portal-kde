%define plasmaver %(echo %{version} |cut -d. -f1-3)
%define stable %([ "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
%define git 20230606

Name: plasma6-xdg-desktop-portal-kde
Version:	5.240.0
Release:	%{?git:0.%{git}.}1
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/xdg-desktop-portal-kde/-/archive/master/xdg-desktop-portal-kde-master.tar.bz2#/xdg-desktop-portal-kde-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/plasma/%{plasmaver}/%{name}-%{version}.tar.xz
%endif
Summary: Backend implementation for xdg-desktop-portal using Qt/KDE
URL: http://kde.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6KIO)
BuildRequires: cmake(KF6Notifications)
BuildRequires: cmake(KF6Wayland)
BuildRequires: cmake(KF6WindowSystem)
BuildRequires: cmake(KF6WidgetsAddons)
BuildRequires: cmake(KF6Declarative)
BuildRequires: cmake(KF6Kirigami2)
BuildRequires: cmake(KF6Plasma)
BuildRequires: cmake(KF6GlobalAccel)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6PrintSupport)
BuildRequires: cmake(Qt6QuickWidgets)
BuildRequires: cmake(Qt6QuickControls2)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6Test)
BuildRequires: cups-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libpipewire-0.3)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: cmake(PlasmaWaylandProtocols)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(epoxy)
Requires: xdg-desktop-portal
Provides: xdg-desktop-portal-implementation

%description
Backend implementation for xdg-desktop-portal using Qt/KDE.

%prep
%autosetup -p1 -n xdg-desktop-portal-kde-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
%find_lang %{name} --all-name --with-html

%post
%systemd_user_post plasma-xdg-desktop-portal-kde.service

%postun
%systemd_user_postun plasma-xdg-desktop-portal-kde.service

%files -f %{name}.lang
%{_libdir}/libexec/xdg-desktop-portal-kde
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.kde.service
%{_datadir}/xdg-desktop-portal
%{_datadir}/applications/org.freedesktop.impl.portal.desktop.kde.desktop
%{_datadir}/knotifications6/xdg-desktop-portal-kde.notifyrc
%{_userunitdir}/plasma-xdg-desktop-portal-kde.service
%{_datadir}/qlogging-categories6/xdp-kde.categories
