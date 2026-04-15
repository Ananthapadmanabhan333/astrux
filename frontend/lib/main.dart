import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:math';
import 'package:image_picker/image_picker.dart';

const String apiUrl = String.fromEnvironment('API_URL', defaultValue: 'http://127.0.0.1:8000');

// ─── COSMIC COLOR PALETTE ─────────────────────────────────────────────────
const kDeepSpace   = Color(0xFF080618);
const kNebulaPurple= Color(0xFF1A0B3E);
const kCosmicViolet= Color(0xFF2D1B69);
const kStarDust    = Color(0xFF6B45C5);
const kGold        = Color(0xFFD4AF37);
const kGoldLight   = Color(0xFFFFE066);
const kLavender    = Color(0xFFC5B4E3);
const kWhiteGlow   = Color(0xFFEEE8FF);

void main() {
  runApp(const AstroApp());
}

class AstroApp extends StatelessWidget {
  const AstroApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Astrux — Unlocking Your Cosmic Blueprint',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: kGold,
        scaffoldBackgroundColor: kDeepSpace,
        colorScheme: const ColorScheme.dark(
          primary: kGold,
          secondary: kLavender,
          surface: kCosmicViolet,
        ),
        inputDecorationTheme: InputDecorationTheme(
          labelStyle: const TextStyle(color: kLavender, fontSize: 13),
          filled: true,
          fillColor: Colors.white.withOpacity(0.05),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: kGold.withOpacity(0.3)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: kGold, width: 1.5),
          ),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
          centerTitle: true,
        ),
      ),
      home: const SplashScreen(),
    );
  }
}

// ─── SPLASH SCREEN ────────────────────────────────────────────────────────
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});
  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with TickerProviderStateMixin {
  late AnimationController _rotateCtrl;
  late AnimationController _pulseCtrl;
  late Animation<double> _pulseAnim;

  @override
  void initState() {
    super.initState();
    _rotateCtrl = AnimationController(vsync: this, duration: const Duration(seconds: 20))
      ..repeat();
    _pulseCtrl = AnimationController(vsync: this, duration: const Duration(seconds: 2))
      ..repeat(reverse: true);
    _pulseAnim = Tween<double>(begin: 0.9, end: 1.1).animate(
      CurvedAnimation(parent: _pulseCtrl, curve: Curves.easeInOut));
  }

  @override
  void dispose() {
    _rotateCtrl.dispose();
    _pulseCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kDeepSpace,
      body: Stack(
        children: [
          // ── Cosmic background image
          Positioned.fill(
            child: Image.asset('assets/cosmic_bg.png', fit: BoxFit.cover,
              errorBuilder: (_, __, ___) => const SizedBox()),
          ),
          // ── Dark overlay for depth
          Positioned.fill(child: Container(
            decoration: BoxDecoration(
              gradient: RadialGradient(
                center: Alignment.center, radius: 1.2,
                colors: [Colors.transparent, kDeepSpace.withOpacity(0.7), kDeepSpace.withOpacity(0.9)],
              )
            ),
          )),
          // ── Star particles
          const Positioned.fill(child: StarField()),
          // ── Main content
          SafeArea(
            child: Column(
              children: [
                const Spacer(flex: 2),
                // Spinning zodiac ring
                AnimatedBuilder(
                  animation: _rotateCtrl,
                  builder: (_, child) => Transform.rotate(
                    angle: _rotateCtrl.value * 2 * pi, child: child),
                  child: _buildZodiacRing(),
                ),
                const SizedBox(height: 40),
                // ASTRUX title
                ScaleTransition(
                  scale: _pulseAnim,
                  child: ShaderMask(
                    shaderCallback: (b) => const LinearGradient(
                      colors: [kGoldLight, kLavender, kGold],
                    ).createShader(b),
                    child: const Text('ASTRUX',
                      style: TextStyle(fontSize: 56, fontWeight: FontWeight.w900,
                        letterSpacing: 8, color: Colors.white,
                        shadows: [Shadow(color: kGold, blurRadius: 30, offset: Offset(0,0))]),
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                const Text('Unlocking Your Cosmic Blueprint',
                  style: TextStyle(color: kLavender, fontSize: 16,
                    letterSpacing: 2, fontStyle: FontStyle.italic)),
                const Spacer(flex: 2),
                // Navigation pills
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  child: Row(
                    children: [
                      Expanded(child: _CosmicPill(
                        icon: Icons.bar_chart,
                        label: 'Daily Horoscopes\n& Insights',
                        onTap: () => Navigator.push(context,
                          MaterialPageRoute(builder: (_) => const MainLayout())),
                      )),
                      const SizedBox(width: 15),
                      Expanded(child: _CosmicPill(
                        icon: Icons.people,
                        label: 'Join the\nCommunity',
                        onTap: () => Navigator.push(context,
                          MaterialPageRoute(builder: (_) => const MainLayout(startIndex: 2))),
                      )),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
                // Enter button
                GestureDetector(
                  onTap: () => Navigator.pushReplacement(context,
                    MaterialPageRoute(builder: (_) => const MainLayout())),
                  child: Container(
                    margin: const EdgeInsets.symmetric(horizontal: 50),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(colors: [kCosmicViolet, kStarDust]),
                      borderRadius: BorderRadius.circular(40),
                      border: Border.all(color: kGold.withOpacity(0.6), width: 1.5),
                      boxShadow: [BoxShadow(color: kGold.withOpacity(0.3), blurRadius: 20, spreadRadius: 2)],
                    ),
                    child: const Center(
                      child: Text('BEGIN YOUR READING',
                        style: TextStyle(color: kGoldLight, fontSize: 14,
                          fontWeight: FontWeight.bold, letterSpacing: 2)),
                    ),
                  ),
                ),
                const SizedBox(height: 40),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildZodiacRing() {
    return SizedBox(
      width: 200, height: 200,
      child: CustomPaint(painter: ZodiacRingPainter()),
    );
  }
}

class _CosmicPill extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;
  const _CosmicPill({required this.icon, required this.label, required this.onTap});
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.05),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: kGold.withOpacity(0.4)),
          boxShadow: [BoxShadow(color: kStarDust.withOpacity(0.15), blurRadius: 15)],
        ),
        child: Column(
          children: [
            Icon(icon, color: kGold, size: 28),
            const SizedBox(height: 8),
            Text(label, textAlign: TextAlign.center,
              style: const TextStyle(color: kWhiteGlow, fontSize: 13, height: 1.4)),
          ],
        ),
      ),
    );
  }
}

// ─── STAR FIELD PAINTER ───────────────────────────────────────────────────
class StarField extends StatefulWidget {
  const StarField({super.key});
  @override
  State<StarField> createState() => _StarFieldState();
}

class _StarFieldState extends State<StarField> with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  final List<_Star> _stars = List.generate(100, (_) => _Star());

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 3))
      ..repeat(reverse: true);
    _ctrl.addListener(() => setState(() {}));
  }
  @override
  void dispose() { _ctrl.dispose(); super.dispose(); }
  @override
  Widget build(BuildContext context) {
    return CustomPaint(painter: _StarPainter(_stars, _ctrl.value));
  }
}

class _Star {
  final double x = Random().nextDouble();
  final double y = Random().nextDouble();
  final double size = Random().nextDouble() * 2 + 0.5;
  final double phase = Random().nextDouble();
}

class _StarPainter extends CustomPainter {
  final List<_Star> stars;
  final double t;
  _StarPainter(this.stars, this.t);
  @override
  void paint(Canvas canvas, Size size) {
    for (final s in stars) {
      final opacity = (0.3 + 0.7 * ((sin((t + s.phase) * pi)).abs())).clamp(0.1, 1.0);
      canvas.drawCircle(
        Offset(s.x * size.width, s.y * size.height),
        s.size,
        Paint()..color = kWhiteGlow.withOpacity(opacity),
      );
    }
  }
  @override bool shouldRepaint(_StarPainter old) => old.t != t;
}

// ─── ZODIAC RING PAINTER ──────────────────────────────────────────────────
class ZodiacRingPainter extends CustomPainter {
  final List<String> symbols = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'];
  @override
  void paint(Canvas canvas, Size size) {
    final cx = size.width / 2;
    final cy = size.height / 2;
    final r  = size.width / 2 - 10;

    // Outer ring
    canvas.drawCircle(Offset(cx, cy), r,
      Paint()..color = kGold.withOpacity(0.25)..style = PaintingStyle.stroke..strokeWidth = 1);
    canvas.drawCircle(Offset(cx, cy), r - 12,
      Paint()..color = kGold.withOpacity(0.15)..style = PaintingStyle.stroke..strokeWidth = 1);

    // Draw armillary sphere rings manually
    final ringPaint = Paint()..color = kGold.withOpacity(0.6)..style = PaintingStyle.stroke..strokeWidth = 3..strokeCap = StrokeCap.round;
    canvas.drawCircle(Offset(cx, cy), r * 0.5, ringPaint);
    canvas.save();
    canvas.translate(cx, cy);
    canvas.rotate(pi / 4);
    canvas.drawOval(Rect.fromCenter(center: Offset.zero, width: r, height: r * 0.4), ringPaint);
    canvas.rotate(pi / 2);
    canvas.drawOval(Rect.fromCenter(center: Offset.zero, width: r, height: r * 0.4), ringPaint);
    canvas.restore();

    // Zodiac symbols
    final tp = TextPainter(textDirection: TextDirection.ltr);
    for (int i = 0; i < 12; i++) {
      final angle = (i * 30 - 90) * pi / 180;
      final sx = cx + r * 0.82 * cos(angle);
      final sy = cy + r * 0.82 * sin(angle);
      tp.text = TextSpan(text: symbols[i],
        style: TextStyle(color: kGold.withOpacity(0.85), fontSize: 13, fontWeight: FontWeight.bold));
      tp.layout();
      tp.paint(canvas, Offset(sx - tp.width / 2, sy - tp.height / 2));
    }
  }
  @override bool shouldRepaint(covariant CustomPainter _) => false;
}

// ─── MAIN LAYOUT ──────────────────────────────────────────────────────────
class MainLayout extends StatefulWidget {
  final int startIndex;
  const MainLayout({super.key, this.startIndex = 0});

  @override
  State<MainLayout> createState() => _MainLayoutState();
}

class _MainLayoutState extends State<MainLayout> {
  late int _currentIndex;
  Map<String, dynamic>? globalChartData;
  late final List<Widget> _pages;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.startIndex;
    _pages = [
      HomeDashboard(getChart: () => globalChartData),
      KundaliEngine(onChartGenerated: (data) => setState(() => globalChartData = data)),
      const KundaliMatching(),
      const PanchangTab(),
      const PalmistryTab(),
      AIAstrologerChat(getChart: () => globalChartData),
    ];
  }

  void _showCallSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: kNebulaPurple,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (context) => Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
          border: Border(top: BorderSide(color: kGold.withOpacity(0.4), width: 1)),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(width: 40, height: 3, decoration: BoxDecoration(color: kGold.withOpacity(0.4), borderRadius: BorderRadius.circular(2))),
            const SizedBox(height: 20),
            ShaderMask(
              shaderCallback: (b) => const LinearGradient(colors: [kGoldLight, kLavender]).createShader(b),
              child: const Text("Consult Premium Astrologers", style: TextStyle(fontSize: 20, color: Colors.white, fontWeight: FontWeight.bold, letterSpacing: 1)),
            ),
            const SizedBox(height: 20),
            _buildAstrologerTile("Acharya Sharma", "Vedic, Vastu", "4.9", "\$2/min", true),
            _buildAstrologerTile("Dr. Nandini", "Tarot, Numerology", "4.8", "\$3/min", false),
            _buildAstrologerTile("Pandit Vyas", "Kundali Milan, Prashna", "5.0", "\$5/min", true),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  Widget _buildAstrologerTile(String name, String skills, String rating, String price, bool online) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: online ? kGold.withOpacity(0.3) : Colors.white12),
      ),
      child: Row(children: [
        CircleAvatar(
          backgroundColor: online ? kGold.withOpacity(0.15) : Colors.white10,
          child: Icon(Icons.person, color: online ? kGold : Colors.grey, size: 20),
        ),
        const SizedBox(width: 12),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(name, style: const TextStyle(color: kWhiteGlow, fontWeight: FontWeight.bold, fontSize: 15)),
          Text("$skills • $price", style: const TextStyle(color: kLavender, fontSize: 12)),
        ])),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 2, vertical: 2),
          child: Row(mainAxisSize: MainAxisSize.min, children: [
            Container(width: 8, height: 8, decoration: BoxDecoration(color: online ? Colors.greenAccent : Colors.grey, shape: BoxShape.circle)),
            const SizedBox(width: 6),
            Text(online ? "Online" : "Offline", style: TextStyle(color: online ? Colors.greenAccent : Colors.grey, fontSize: 11)),
          ]),
        ),
        const SizedBox(width: 8),
        ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: online ? kCosmicViolet : Colors.grey.shade800,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            side: online ? BorderSide(color: kGold.withOpacity(0.5)) : BorderSide.none,
          ),
          onPressed: online ? () {} : null,
          child: Row(mainAxisSize: MainAxisSize.min, children: [
            Icon(Icons.call, size: 14, color: online ? kGoldLight : Colors.grey),
            const SizedBox(width: 4),
            Text("Call", style: TextStyle(color: online ? kGoldLight : Colors.grey, fontSize: 12)),
          ]),
        ),
      ]),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kDeepSpace,
      body: Stack(
        children: [
          // Cosmic starfield background
          Positioned.fill(child: Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [kDeepSpace, kNebulaPurple, Color(0xFF130830)],
                begin: Alignment.topCenter, end: Alignment.bottomCenter,
              ),
            ),
          )),
          const Positioned.fill(child: StarField()),
          // Nebula glow accent
          Positioned(top: -100, right: -100, child: Container(
            width: 350, height: 350,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: RadialGradient(colors: [kStarDust.withOpacity(0.12), Colors.transparent]),
            ),
          )),
          SafeArea(child: _pages[_currentIndex]),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: kCosmicViolet,
        icon: const Icon(Icons.call, color: kGoldLight),
        label: const Text("Consult", style: TextStyle(color: kGoldLight, fontWeight: FontWeight.bold, letterSpacing: 1)),
        onPressed: () => _showCallSheet(context),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30),
          side: BorderSide(color: kGold.withOpacity(0.5))
        ),
      ),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: kDeepSpace,
          border: Border(top: BorderSide(color: kGold.withOpacity(0.2), width: 1)),
          boxShadow: [BoxShadow(color: kStarDust.withOpacity(0.15), blurRadius: 20, offset: const Offset(0, -5))],
        ),
        child: BottomNavigationBar(
          backgroundColor: Colors.transparent,
          selectedItemColor: kGold,
          unselectedItemColor: Colors.white30,
          currentIndex: _currentIndex,
          onTap: (i) => setState(() => _currentIndex = i),
          type: BottomNavigationBarType.fixed,
          elevation: 0,
          selectedLabelStyle: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold, letterSpacing: 0.5),
          unselectedLabelStyle: const TextStyle(fontSize: 10),
          items: const [
            BottomNavigationBarItem(icon: Icon(Icons.auto_awesome, size: 22), label: 'Home'),
            BottomNavigationBarItem(icon: Icon(Icons.pie_chart_outline, size: 22), label: 'Chart'),
            BottomNavigationBarItem(icon: Icon(Icons.favorite, size: 22), label: 'Match'),
            BottomNavigationBarItem(icon: Icon(Icons.calendar_month, size: 22), label: 'Panchang'),
            BottomNavigationBarItem(icon: Icon(Icons.back_hand, size: 22), label: 'Palm'),
            BottomNavigationBarItem(icon: Icon(Icons.psychology, size: 22), label: 'AI'),
          ],
        ),
      ),
    );
  }
}


// --- HOME DASHBOARD ---
class HomeDashboard extends StatefulWidget {
  final Map<String, dynamic>? Function() getChart;
  const HomeDashboard({super.key, required this.getChart});

  @override
  State<HomeDashboard> createState() => _HomeDashboardState();
}

class _HomeDashboardState extends State<HomeDashboard> {
  Map<String, dynamic>? dailyPrediction;

  @override
  void initState() {
    super.initState();
    _loadDaily();
  }

  void _loadDaily() async {
    final chart = widget.getChart();
    String lagna = chart != null ? chart['lagna'] : "Aries";
    try {
      final res = await http.get(Uri.parse('$apiUrl/daily-prediction?lagna=$lagna'));
      if (res.statusCode == 200) {
        setState(() => dailyPrediction = jsonDecode(res.body));
      }
    } catch(e) {
      // Ignored for UI
    }
  }

  @override
  Widget build(BuildContext context) {
    final chart = widget.getChart();
    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 20, 20, 100),
      children: [
        // ── Header
        Row(children: [
          ShaderMask(
            shaderCallback: (b) => const LinearGradient(colors: [kGoldLight, kLavender, kGold]).createShader(b),
            child: const Text('✦ ASTRUX', style: TextStyle(fontSize: 30, fontWeight: FontWeight.w900, color: Colors.white, letterSpacing: 3)),
          ),
          const Spacer(),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration: BoxDecoration(
              color: kGold.withOpacity(0.1),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: kGold.withOpacity(0.35)),
            ),
            child: const Text('VEDIC ENGINE', style: TextStyle(color: kGoldLight, fontSize: 10, letterSpacing: 2)),
          ),
        ]),
        const SizedBox(height: 4),
        const Text('Unlocking Your Cosmic Blueprint', style: TextStyle(color: kLavender, fontSize: 12, letterSpacing: 1, fontStyle: FontStyle.italic)),
        const SizedBox(height: 24),

        // ── No chart prompt
        if (chart == null)
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: kGold.withOpacity(0.3)),
              gradient: LinearGradient(colors: [kNebulaPurple.withOpacity(0.6), kCosmicViolet.withOpacity(0.4)]),
            ),
            child: Column(children: [
              const Icon(Icons.auto_awesome, color: kGold, size: 32),
              const SizedBox(height: 12),
              const Text('Your Cosmic Blueprint Awaits', style: TextStyle(color: kWhiteGlow, fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              const Text('Go to the Chart tab → enter your birth details → tap Generate to unveil your complete Vedic astrology report.', textAlign: TextAlign.center, style: TextStyle(color: kLavender, height: 1.5, fontSize: 13)),
            ]),
          ),

        // ── Dasha banner
        if (chart != null) ...[
          Container(
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(20),
              gradient: const LinearGradient(colors: [Color(0xFF3A2070), Color(0xFF1A0B3E)], begin: Alignment.topLeft, end: Alignment.bottomRight),
              border: Border.all(color: kGold.withOpacity(0.4)),
              boxShadow: [BoxShadow(color: kGold.withOpacity(0.15), blurRadius: 20, spreadRadius: 1)],
            ),
            child: Row(children: [
              Expanded(child: _buildMetricBlock('Lagna', chart['lagna'] ?? 'N/A')),
              Container(height: 50, width: 1, color: kGold.withOpacity(0.3)),
              Expanded(child: _buildMetricBlock('Mahadasha', (chart['current_dasha'] ?? 'N/A').toString().replaceAll(' Mahadasha', ''))),
              if (chart['dasha_detail'] != null && chart['dasha_detail']['antardasha'] != null) ...[
                Container(height: 50, width: 1, color: kGold.withOpacity(0.3)),
                Expanded(child: _buildMetricBlock('Antardasha', chart['dasha_detail']['antardasha'] ?? 'N/A')),
              ],
            ]),
          ),
          const SizedBox(height: 30),

          // ── Report header
          Row(children: [
            const Icon(Icons.auto_awesome, color: kGold, size: 18),
            const SizedBox(width: 8),
            const Text('Full Vedic Analysis Report', style: TextStyle(color: kWhiteGlow, fontSize: 18, fontWeight: FontWeight.bold)),
          ]),
          const SizedBox(height: 4),
          const Text('Brihat Parashara Hora Shastra · Classical Jyotish', style: TextStyle(color: kLavender, fontSize: 10, letterSpacing: 1.5)),
          const SizedBox(height: 16),

          // ── Insight cards
          ...(chart['insights'] as List? ?? []).map((i) {
            final type = i['type'] ?? '';
            final isDosha  = type == 'dosha' || type == 'sadesati';
            final isYoga   = type == 'yoga' || type == 'raj_yoga';
            final isGem    = type == 'gemstone';
            final isNak    = type == 'nakshatra';
            final isKarmic = type == 'karmic';
            final isLagna  = type == 'lagna';
            final isDasha  = type == 'dasha';
            final isHouse  = type == 'house_lord';

            final Color accent =
              isDosha  ? const Color(0xFFFF6B6B) :
              isYoga   ? const Color(0xFFFFD166) :
              isGem    ? const Color(0xFF4ECDC4) :
              isNak    ? const Color(0xFFBB8FFF) :
              isKarmic ? const Color(0xFFFF9F43) :
              isLagna  ? kGoldLight :
              isDasha  ? const Color(0xFF74B9FF) :
              isHouse  ? const Color(0xFF55EFC4) :
              const Color(0xFFA8E6CF);

            final IconData icon =
              isDosha  ? Icons.warning_amber_rounded :
              isYoga   ? Icons.auto_awesome :
              isGem    ? Icons.diamond :
              isNak    ? Icons.stars :
              isKarmic ? Icons.loop :
              isLagna  ? Icons.person :
              isDasha  ? Icons.access_time :
              isHouse  ? Icons.home_work :
              Icons.check_circle_outline;

            return Container(
              margin: const EdgeInsets.only(bottom: 14),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: accent.withOpacity(0.3), width: 1),
                gradient: LinearGradient(
                  colors: [kNebulaPurple.withOpacity(0.7), kDeepSpace.withOpacity(0.8)],
                  begin: Alignment.topLeft, end: Alignment.bottomRight,
                ),
                boxShadow: [BoxShadow(color: accent.withOpacity(0.08), blurRadius: 12, spreadRadius: 1)],
              ),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                    color: accent.withOpacity(0.08),
                    border: Border(bottom: BorderSide(color: accent.withOpacity(0.15))),
                  ),
                  child: Row(children: [
                    Container(
                      padding: const EdgeInsets.all(7),
                      decoration: BoxDecoration(
                        color: accent.withOpacity(0.15),
                        shape: BoxShape.circle,
                        border: Border.all(color: accent.withOpacity(0.3)),
                      ),
                      child: Icon(icon, color: accent, size: 16),
                    ),
                    const SizedBox(width: 10),
                    Expanded(child: Text(i['title'], style: TextStyle(fontWeight: FontWeight.bold, color: accent, fontSize: 13, letterSpacing: 0.3))),
                  ]),
                ),
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Text(i['description'], style: const TextStyle(color: kLavender, height: 1.75, fontSize: 12.5)),
                ),
              ]),
            );
          }).toList(),
        ],

        const SizedBox(height: 20),

        // ── Daily transits
        Row(children: [
          const Icon(Icons.wb_sunny_outlined, color: kGold, size: 18),
          const SizedBox(width: 8),
          const Text('Daily Transits', style: TextStyle(color: kWhiteGlow, fontSize: 18, fontWeight: FontWeight.bold)),
        ]),
        const SizedBox(height: 12),
        if (dailyPrediction != null)
          ...dailyPrediction!.entries.map((e) => Container(
            margin: const EdgeInsets.only(bottom: 10),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(14),
              gradient: LinearGradient(colors: [kNebulaPurple.withOpacity(0.5), kDeepSpace.withOpacity(0.7)]),
              border: Border.all(color: kGold.withOpacity(0.15)),
            ),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                Icon(_transitIcon(e.key), color: kGold, size: 16),
                const SizedBox(width: 8),
                Text(e.key, style: const TextStyle(color: kGoldLight, fontWeight: FontWeight.bold, fontSize: 13, letterSpacing: 0.5)),
              ]),
              const SizedBox(height: 8),
              Text(e.value.toString(), style: const TextStyle(color: kLavender, height: 1.5, fontSize: 12.5)),
            ]),
          )),
      ],
    );
  }

  IconData _transitIcon(String key) {
    switch (key.toLowerCase()) {
      case 'career': return Icons.work_outline;
      case 'love': return Icons.favorite_border;
      case 'finance': return Icons.account_balance_wallet_outlined;
      case 'health': return Icons.monitor_heart_outlined;
      default: return Icons.star_outline;
    }
  }

  Widget _buildMetricBlock(String title, String val) {
    return Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Text(title.toUpperCase(), style: TextStyle(color: kGold.withOpacity(0.7), fontSize: 9, fontWeight: FontWeight.bold, letterSpacing: 1.5)),
      const SizedBox(height: 4),
      Text(val, style: const TextStyle(color: kGoldLight, fontSize: 16, fontWeight: FontWeight.w900), textAlign: TextAlign.center),
    ]);
  }
}


// --- KUNDALI ENGINE ---
class KundaliEngine extends StatefulWidget {
  final Function(Map<String, dynamic>) onChartGenerated;
  const KundaliEngine({super.key, required this.onChartGenerated});

  @override
  State<KundaliEngine> createState() => _KundaliEngineState();
}

class _KundaliEngineState extends State<KundaliEngine> {
  bool _isLoading = false;
  Map<String, dynamic>? _chartData;
  
  final _dob = TextEditingController(text: "1995-10-24");
  final _tob = TextEditingController(text: "14:30");
  final _lat = TextEditingController(text: "28.6139");
  final _lon = TextEditingController(text: "77.2090");

  void _generate() async {
    setState(() => _isLoading = true);
    try {
      final res = await http.post(
        Uri.parse('$apiUrl/generate-chart'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          "date_of_birth": _dob.text,
          "time_of_birth": _tob.text,
          "latitude": double.parse(_lat.text),
          "longitude": double.parse(_lon.text)
        })
      );
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        setState(() => _chartData = data);
        widget.onChartGenerated(data);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: ${res.body}')));
      }
    } catch(e) {
       ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Network Error: Make sure backend is running.')));
    } finally {
      if(mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("Advanced Chart Engine", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 1.2)),
          const SizedBox(height: 5),
          const Text("Enter precision birth details to calculate accurate celestial coordinates.", style: TextStyle(color: Colors.white54, fontSize: 14)),
          const SizedBox(height: 25),
          
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: const Color(0xFF1E1A3C),
              borderRadius: BorderRadius.circular(20),
              boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 10, offset: Offset(0, 5))],
              border: Border.all(color: const Color(0x33FFD700))
            ),
            child: Column(
              children: [
                Row(
                  children: [
                    Expanded(child: _buildInput(_dob, "DOB (YYYY-MM-DD)", Icons.calendar_today)),
                    const SizedBox(width: 15),
                    Expanded(child: _buildInput(_tob, "Time (HH:MM)", Icons.access_time)),
                  ],
                ),
                const SizedBox(height: 15),
                Row(
                  children: [
                    Expanded(child: _buildInput(_lat, "Latitude (e.g. 28.6)", Icons.public)),
                    const SizedBox(width: 15),
                    Expanded(child: _buildInput(_lon, "Longitude (e.g. 77.2)", Icons.explore)),
                  ],
                ),
                const SizedBox(height: 25),
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFFFD700),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      elevation: 5,
                    ),
                    onPressed: _isLoading ? null : _generate,
                    icon: _isLoading ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2)) : const Icon(Icons.rocket_launch, color: Colors.black),
                    label: Text(_isLoading ? "CALCULATING ORBITS..." : "GENERATE PRECISION CHART", style: const TextStyle(color: Colors.black, fontSize: 16, fontWeight: FontWeight.bold, letterSpacing: 1.1)),
                  ),
                ),
              ],
            )
          ),
          const SizedBox(height: 40),
          if (_chartData != null) ...[
             const Text("Vedic Birth Chart (Lagna Kundali)", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Color(0xFFFFD700))),
             const SizedBox(height: 20),
             Center(
               child: Container(
                 width: 320,
                 height: 320,
                 decoration: BoxDecoration(
                   color: const Color(0xFFFAF1E4),
                   borderRadius: BorderRadius.circular(10),
                   border: Border.all(color: const Color(0xFFD4AF37), width: 3),
                   boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 15, offset: Offset(0, 5))],
                 ),
                 child: CustomPaint(
                    painter: NorthIndianChartPainter(_chartData!['planets'] ?? []),
                    size: const Size(320, 320),
                 ),
               ),
             ),
             const SizedBox(height: 40),
             const Text("Detailed Planetary Positions", style: TextStyle(color: Color(0xFFFFD700), fontSize: 22, fontWeight: FontWeight.bold)),
             const SizedBox(height: 15),
             ListView.builder(
               shrinkWrap: true,
               physics: const NeverScrollableScrollPhysics(),
               itemCount: (_chartData!['planets'] as List).length,
               itemBuilder: (context, index) {
                 final p = _chartData!['planets'][index];
                 final bool isRetro = p['retrograde'] == true;
                 return Container(
                   margin: const EdgeInsets.only(bottom: 12),
                   padding: const EdgeInsets.all(15),
                   decoration: BoxDecoration(
                     color: const Color(0xFF1E1A3C),
                     borderRadius: BorderRadius.circular(15),
                     border: Border.all(color: Colors.white12),
                   ),
                   child: Row(
                     children: [
                       Container(
                         padding: const EdgeInsets.all(12),
                         decoration: const BoxDecoration(
                           color: Color(0x22FFD700),
                           shape: BoxShape.circle,
                         ),
                         child: Text(p['name'].substring(0, 2).toUpperCase(), style: const TextStyle(color: Color(0xFFFFD700), fontWeight: FontWeight.bold, fontSize: 16)),
                       ),
                       const SizedBox(width: 15),
                       Expanded(
                         child: Column(
                           crossAxisAlignment: CrossAxisAlignment.start,
                           children: [
                             Row(
                               children: [
                                 Text("${p['name']}", style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w600)),
                                 if (isRetro) ...[
                                   const SizedBox(width: 10),
                                   Container(padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2), decoration: BoxDecoration(color: Colors.redAccent.withOpacity(0.2), borderRadius: BorderRadius.circular(10)), child: const Text("Retro", style: TextStyle(color: Colors.redAccent, fontSize: 10, fontWeight: FontWeight.bold))),
                                 ]
                               ],
                             ),
                             const SizedBox(height: 5),
                             Text("Sign: ${p['sign']} • House: ${p['house']} • Deg: ${p['degree']}°", style: const TextStyle(color: Colors.white70, fontSize: 13)),
                             const SizedBox(height: 3),
                             Text("Nakshatra: ${p['nakshatra']} (Pada ${p['pada']})", style: const TextStyle(color: Colors.white54, fontSize: 12)),
                           ],
                         ),
                       ),
                       const Icon(Icons.stars, color: Color(0x55FFD700), size: 30),
                     ],
                   )
                 );
               }
             )
          ]
        ],
      ),
    );
  }

  Widget _buildInput(TextEditingController ctrl, String hint, IconData icon) {
    return TextField(
      controller: ctrl,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: hint,
        labelStyle: const TextStyle(color: Colors.white54, fontSize: 13),
        prefixIcon: Icon(icon, color: const Color(0xFFFFD700), size: 20),
        filled: true,
        fillColor: const Color(0x22000000),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Colors.white12)),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFFFD700))),
      )
    );
  }
}

class NorthIndianChartPainter extends CustomPainter {
  final List<dynamic> planets;
  NorthIndianChartPainter(this.planets);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = Colors.black..strokeWidth = 2.0..style = PaintingStyle.stroke;
    final w = size.width;
    final h = size.height;

    // Outer box
    canvas.drawRect(Rect.fromLTWH(0, 0, w, h), paint);
    // Diagonals
    canvas.drawLine(const Offset(0, 0), Offset(w, h), paint);
    canvas.drawLine(Offset(w, 0), Offset(0, h), paint);
    // Diamond
    canvas.drawLine(Offset(w/2, 0), Offset(w, h/2), paint);
    canvas.drawLine(Offset(w, h/2), Offset(w/2, h), paint);
    canvas.drawLine(Offset(w/2, h), Offset(0, h/2), paint);
    canvas.drawLine(Offset(0, h/2), Offset(w/2, 0), paint);

    // Labels for houses loosely placed
    final tp = TextPainter(textDirection: TextDirection.ltr);
    
    // Quick house map logic: Just list planet abbreviations in house boxes
    Map<int, List<String>> housePlanets = {};
    for (var p in planets) {
      if(!housePlanets.containsKey(p['house'])) housePlanets[p['house']] = [];
      housePlanets[p['house']]!.add(p['name'].substring(0, 2)); 
    }

    // Rough approximate centers for the 12 houses in a North Indian chart
    List<Offset> centers = [
      Offset(w/2, h/4), Offset(w/4, h/4-20), Offset(w/4-20, h/4), 
      Offset(w/2-20, h/2), Offset(w/4-20, 3*h/4), Offset(w/4, 3*h/4+20),
      Offset(w/2, 3*h/4), Offset(3*w/4, 3*h/4+20), Offset(3*w/4+20, 3*h/4),
      Offset(w/2+20, h/2), Offset(3*w/4+20, h/4), Offset(3*w/4, h/4-20)
    ];

    for (int i=1; i<=12; ++i) {
      String text = housePlanets[i]?.join(",") ?? "";
      if (text.isNotEmpty) {
        tp.text = TextSpan(text: text, style: const TextStyle(color: Colors.red, fontSize: 12, fontWeight: FontWeight.bold));
        tp.layout();
        tp.paint(canvas, centers[i-1] - Offset(tp.width/2, tp.height/2));
      }
    }
  }
  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}

// --- KUNDALI MATCHING ---
class KundaliMatching extends StatefulWidget {
  const KundaliMatching({super.key});
  @override
  State<KundaliMatching> createState() => _KundaliMatchingState();
}

class _KundaliMatchingState extends State<KundaliMatching> {
  final _bdob  = TextEditingController(text: "1995-10-24");
  final _btob  = TextEditingController(text: "14:30");
  final _blat  = TextEditingController(text: "28.6139");
  final _blon  = TextEditingController(text: "77.2090");
  final _gdob  = TextEditingController(text: "1998-05-15");
  final _gtob  = TextEditingController(text: "10:00");
  final _glat  = TextEditingController(text: "19.0760");
  final _glon  = TextEditingController(text: "72.8777");
  Map<String, dynamic>? _result;
  bool _isLoading = false;

  void _match() async {
    setState(() => _isLoading = true);
    try {
      final res = await http.post(
        Uri.parse('$apiUrl/match'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          "boy_dob": _bdob.text, "boy_tob": _btob.text,
          "boy_lat": double.tryParse(_blat.text) ?? 28.6,
          "boy_lon": double.tryParse(_blon.text) ?? 77.2,
          "girl_dob": _gdob.text, "girl_tob": _gtob.text,
          "girl_lat": double.tryParse(_glat.text) ?? 19.0,
          "girl_lon": double.tryParse(_glon.text) ?? 72.8,
        }),
      );
      if (mounted && res.statusCode == 200) setState(() => _result = jsonDecode(res.body));
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final match = _result?['match'];
    final boy   = _result?['boy'];
    final girl  = _result?['girl'];

    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 20, 20, 100),
      children: [
        // Header
        ShaderMask(
          shaderCallback: (b) => const LinearGradient(colors: [kGoldLight, kLavender]).createShader(b),
          child: const Text('💑 Kundali Milan', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: Colors.white, letterSpacing: 1.5)),
        ),
        const SizedBox(height: 4),
        const Text('Ashtakoot Guna Milan · Vedic Marriage Compatibility', style: TextStyle(color: kLavender, fontSize: 12, letterSpacing: 1, fontStyle: FontStyle.italic)),
        const SizedBox(height: 24),

        // ── Input forms
        _buildPersonForm('👦 Boy / Groom', kCosmicViolet, _bdob, _btob, _blat, _blon, Colors.lightBlueAccent),
        const SizedBox(height: 16),
        _buildPersonForm('👧 Girl / Bride', const Color(0xFF3D0B55), _gdob, _gtob, _glat, _glon, Colors.pinkAccent),
        const SizedBox(height: 20),

        // Generate button
        GestureDetector(
          onTap: _isLoading ? null : _match,
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 16),
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [kCosmicViolet, kStarDust]),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: kGold.withOpacity(0.5)),
              boxShadow: [BoxShadow(color: kGold.withOpacity(0.2), blurRadius: 20)],
            ),
            child: Center(child: _isLoading
              ? const Row(mainAxisSize: MainAxisSize.min, children: [
                  SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: kGoldLight, strokeWidth: 2)),
                  SizedBox(width: 12),
                  Text('COMPUTING COSMIC ALIGNMENT...', style: TextStyle(color: kGoldLight, fontWeight: FontWeight.bold, letterSpacing: 1)),
                ])
              : const Row(mainAxisSize: MainAxisSize.min, children: [
                  Icon(Icons.favorite, color: Colors.pinkAccent, size: 18),
                  SizedBox(width: 10),
                  Text('GENERATE COMPATIBILITY REPORT', style: TextStyle(color: kGoldLight, fontWeight: FontWeight.bold, fontSize: 14, letterSpacing: 1)),
                ]),
            ),
          ),
        ),

        if (_result != null && match != null) ...[
          const SizedBox(height: 32),

          // ── Score ring
          _buildScoreRing(match['score'] as int, match['status'] as String),
          const SizedBox(height: 24),

          // ── Partner profile cards
          Row(children: [
            Expanded(child: _buildProfileCard('Boy', boy, Colors.lightBlueAccent)),
            const SizedBox(width: 12),
            Expanded(child: _buildProfileCard('Girl', girl, Colors.pinkAccent)),
          ]),
          const SizedBox(height: 24),

          // ── Moon relationship
          _buildInfoCard(
            Icons.nightlight_round, 'Moon Sign Relationship', kLavender,
            match['moon_relationship'] ?? '',
          ),
          const SizedBox(height: 12),

          // ── Manglik
          _buildInfoCard(
            Icons.warning_amber_rounded, 'Manglik Dosha Analysis', const Color(0xFFFF6B6B),
            match['manglik_report'] ?? '',
          ),
          const SizedBox(height: 24),

          // ── 8 Kootas
          Row(children: [
            const Icon(Icons.bar_chart, color: kGold, size: 18),
            const SizedBox(width: 8),
            const Text('Ashtakoot Guna Breakdown', style: TextStyle(color: kWhiteGlow, fontSize: 18, fontWeight: FontWeight.bold)),
          ]),
          const Text('8 Cosmic Compatibility Metrics (Total: 36 Points)', style: TextStyle(color: kLavender, fontSize: 11, letterSpacing: 1)),
          const SizedBox(height: 14),
          ...(match['guna_detailed'] as Map? ?? {}).entries.map((e) => _buildGunaBar(e.key, e.value)),

          const SizedBox(height: 28),

          // ── Life report sections
          Row(children: [
            const Icon(Icons.auto_stories, color: kGold, size: 18),
            const SizedBox(width: 8),
            const Text('Detailed Life Compatibility Report', style: TextStyle(color: kWhiteGlow, fontSize: 18, fontWeight: FontWeight.bold)),
          ]),
          const SizedBox(height: 14),
          ..._buildLifeReport(match['life_report'] as Map? ?? {}),
        ],
      ],
    );
  }

  Widget _buildPersonForm(String title, Color bg, TextEditingController dob, TextEditingController tob, TextEditingController lat, TextEditingController lon, Color accent) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        gradient: LinearGradient(colors: [bg.withOpacity(0.8), kDeepSpace.withOpacity(0.9)]),
        border: Border.all(color: accent.withOpacity(0.35)),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(title, style: TextStyle(color: accent, fontWeight: FontWeight.bold, fontSize: 14, letterSpacing: 1)),
        const SizedBox(height: 12),
        Row(children: [
          Expanded(child: _tf(dob, 'DOB (YYYY-MM-DD)', Icons.calendar_today)),
          const SizedBox(width: 10),
          Expanded(child: _tf(tob, 'Time (HH:MM)', Icons.access_time)),
        ]),
        const SizedBox(height: 10),
        Row(children: [
          Expanded(child: _tf(lat, 'Latitude', Icons.public)),
          const SizedBox(width: 10),
          Expanded(child: _tf(lon, 'Longitude', Icons.explore)),
        ]),
      ]),
    );
  }

  Widget _tf(TextEditingController c, String label, IconData icon) {
    return TextField(
      controller: c,
      style: const TextStyle(color: kWhiteGlow, fontSize: 13),
      decoration: InputDecoration(
        labelText: label,
        prefixIcon: Icon(icon, color: kGold, size: 16),
        contentPadding: const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
      ),
    );
  }

  Widget _buildScoreRing(int score, String status) {
    final pct    = score / 36.0;
    final clr    = pct >= 0.78 ? Colors.greenAccent : pct >= 0.61 ? kGold : pct >= 0.5 ? Colors.orangeAccent : Colors.redAccent;

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20),
        gradient: const LinearGradient(colors: [Color(0xFF2A1060), Color(0xFF0B0618)], begin: Alignment.topLeft, end: Alignment.bottomRight),
        border: Border.all(color: kGold.withOpacity(0.4)),
        boxShadow: [BoxShadow(color: kGold.withOpacity(0.1), blurRadius: 25, spreadRadius: 2)],
      ),
      child: Column(children: [
        Stack(alignment: Alignment.center, children: [
          SizedBox(width: 140, height: 140,
            child: CircularProgressIndicator(value: pct, strokeWidth: 12,
              backgroundColor: Colors.white10,
              valueColor: AlwaysStoppedAnimation(clr)),
          ),
          Column(mainAxisSize: MainAxisSize.min, children: [
            Text('$score', style: TextStyle(fontSize: 48, fontWeight: FontWeight.w900, color: clr)),
            const Text('/36', style: TextStyle(color: kLavender, fontSize: 16)),
          ]),
        ]),
        const SizedBox(height: 16),
        Text('GUNA MILAN SCORE', style: TextStyle(color: kGold.withOpacity(0.7), fontSize: 11, letterSpacing: 2)),
        const SizedBox(height: 8),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
          decoration: BoxDecoration(
            color: clr.withOpacity(0.12),
            borderRadius: BorderRadius.circular(30),
            border: Border.all(color: clr.withOpacity(0.4)),
          ),
          child: Text(status.toUpperCase(), style: TextStyle(color: clr, fontWeight: FontWeight.bold, fontSize: 16, letterSpacing: 2)),
        ),
      ]),
    );
  }

  Widget _buildProfileCard(String label, Map? data, Color accent) {
    if (data == null) return const SizedBox();
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        gradient: LinearGradient(colors: [accent.withOpacity(0.08), kDeepSpace.withOpacity(0.9)]),
        border: Border.all(color: accent.withOpacity(0.3)),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(label, style: TextStyle(color: accent, fontWeight: FontWeight.bold, fontSize: 12, letterSpacing: 1)),
        const SizedBox(height: 10),
        _pRow('Lagna', data['lagna'] ?? ''),
        _pRow('Moon Sign', data['moon_sign'] ?? ''),
        _pRow('Moon Nakshatra', data['moon_nak'] ?? ''),
        _pRow('Lagna Lord', data['lagna_lord'] ?? ''),
        _pRow('Current Dasha', (data['current_dasha'] ?? '').toString().replaceAll(' Mahadasha', '')),
        _pRow('Manglik', data['manglik'] == true ? '⚠️ Yes' : '✅ No'),
        _pRow('Rajju', data['rajju'] ?? ''),
      ]),
    );
  }

  Widget _pRow(String k, String v) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 5),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('$k  ', style: const TextStyle(color: kLavender, fontSize: 11)),
        Expanded(child: Text(v, style: const TextStyle(color: kWhiteGlow, fontSize: 11, fontWeight: FontWeight.w600))),
      ]),
    );
  }

  Widget _buildInfoCard(IconData icon, String title, Color accent, String text) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: accent.withOpacity(0.3)),
        gradient: LinearGradient(colors: [kNebulaPurple.withOpacity(0.7), kDeepSpace.withOpacity(0.8)]),
        boxShadow: [BoxShadow(color: accent.withOpacity(0.07), blurRadius: 12)],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Icon(icon, color: accent, size: 16),
          const SizedBox(width: 8),
          Text(title, style: TextStyle(color: accent, fontWeight: FontWeight.bold, fontSize: 13)),
        ]),
        const SizedBox(height: 10),
        Text(text, style: const TextStyle(color: kLavender, height: 1.6, fontSize: 12.5)),
      ]),
    );
  }

  Widget _buildGunaBar(String name, dynamic data) {
    if (data is! Map) return const SizedBox();
    final sc  = (data['score']   as num?)?.toInt() ?? 0;
    final mx  = (data['max']     as num?)?.toInt() ?? 1;
    final pct = (data['percent'] as num?)?.toDouble() ?? 0.0;
    final st  = data['status'] as String? ?? '';
    final desc= data['description'] as String? ?? '';
    final clr = pct >= 75 ? Colors.greenAccent : pct >= 50 ? kGold : pct >= 25 ? Colors.orangeAccent : Colors.redAccent;

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: clr.withOpacity(0.25)),
        gradient: LinearGradient(colors: [kNebulaPurple.withOpacity(0.6), kDeepSpace.withOpacity(0.9)]),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Expanded(child: Text(name, style: const TextStyle(color: kWhiteGlow, fontWeight: FontWeight.bold, fontSize: 13))),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
            decoration: BoxDecoration(color: clr.withOpacity(0.15), borderRadius: BorderRadius.circular(20), border: Border.all(color: clr.withOpacity(0.4))),
            child: Text('$sc/$mx · $st', style: TextStyle(color: clr, fontSize: 11, fontWeight: FontWeight.bold)),
          ),
        ]),
        const SizedBox(height: 8),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: pct / 100,
            minHeight: 6,
            backgroundColor: Colors.white10,
            valueColor: AlwaysStoppedAnimation(clr),
          ),
        ),
        const SizedBox(height: 8),
        Text(desc, style: const TextStyle(color: kLavender, fontSize: 11.5, height: 1.5)),
      ]),
    );
  }

  List<Widget> _buildLifeReport(Map report) {
    final sections = [
      {'key': 'Overall_Compatibility',     'icon': Icons.auto_awesome,           'title': '🌟 Overall Compatibility',        'color': kGoldLight},
      {'key': 'Love_and_Romance',          'icon': Icons.favorite,               'title': '💞 Love & Romance',               'color': Colors.pinkAccent},
      {'key': 'Marriage_and_Partnership',  'icon': Icons.favorite,           'title': '💍 Marriage & Partnership',       'color': const Color(0xFFFFD166)},
      {'key': 'Children_and_Family',       'icon': Icons.child_friendly,         'title': '👶 Children & Family',            'color': const Color(0xFF55EFC4)},
      {'key': 'Career_and_Finance',        'icon': Icons.account_balance_wallet, 'title': '💰 Career & Finance',             'color': const Color(0xFF74B9FF)},
      {'key': 'Health_and_Longevity',      'icon': Icons.monitor_heart,          'title': '❤️‍🩹 Health & Longevity',         'color': const Color(0xFFFF7675)},
      {'key': 'Spiritual_Compatibility',   'icon': Icons.auto_stories,           'title': '🕉️ Spiritual Compatibility',      'color': const Color(0xFFBB8FFF)},
      {'key': 'Remedies_and_Recommendations','icon': Icons.healing,              'title': '🙏 Remedies & Recommendations',   'color': kGold},
    ];

    return sections.map((s) {
      final text = report[s['key']] as String? ?? '';
      if (text.isEmpty) return const SizedBox();
      final color = s['color'] as Color;
      return Container(
        margin: const EdgeInsets.only(bottom: 14),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: color.withOpacity(0.3)),
          gradient: LinearGradient(colors: [kNebulaPurple.withOpacity(0.7), kDeepSpace.withOpacity(0.8)]),
          boxShadow: [BoxShadow(color: color.withOpacity(0.07), blurRadius: 12)],
        ),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: color.withOpacity(0.08),
              borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
              border: Border(bottom: BorderSide(color: color.withOpacity(0.15))),
            ),
            child: Row(children: [
              Container(padding: const EdgeInsets.all(7), decoration: BoxDecoration(color: color.withOpacity(0.15), shape: BoxShape.circle, border: Border.all(color: color.withOpacity(0.3))),
                child: Icon(s['icon'] as IconData, color: color, size: 15)),
              const SizedBox(width: 10),
              Text(s['title'] as String, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 13, letterSpacing: 0.3)),
            ]),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text(text, style: const TextStyle(color: kLavender, height: 1.75, fontSize: 12.5)),
          ),
        ]),
      );
    }).toList();
  }
}


// --- PANCHANG ---
class PanchangTab extends StatefulWidget {
  const PanchangTab({super.key});
  @override
  State<PanchangTab> createState() => _PanchangTabState();
}

class _PanchangTabState extends State<PanchangTab> {
  Map<String, dynamic>? _pData;
  @override
  void initState() {
    super.initState();
    _fetch();
  }
  void _fetch() async {
    final now = DateTime.now();
    final d = "${now.year}-${now.month}-${now.day}";
    try {
      final res = await http.get(Uri.parse('$apiUrl/panchang?date=$d&lat=28.61&lon=77.2'));
      if(mounted && res.statusCode == 200) setState(() => _pData = jsonDecode(res.body));
    } catch(e){}
  }
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        const Text("Live Panchang", style: TextStyle(fontSize: 30, fontWeight: FontWeight.w900, color: Colors.white)),
        const Text("Daily Vedic Timekeeping", style: TextStyle(color: Colors.white54, fontSize: 14)),
        const SizedBox(height: 30),
        if (_pData != null) ...[
          GridView.count(
            crossAxisCount: 2,
            crossAxisSpacing: 15,
            mainAxisSpacing: 15,
            shrinkWrap: true,
            childAspectRatio: 1.5,
            physics: const NeverScrollableScrollPhysics(),
            children: [
              _buildPanchangCard("Tithi", _pData!['tithi'], Icons.nightlight_round),
              _buildPanchangCard("Nakshatra", _pData!['nakshatra'], Icons.star),
              _buildPanchangCard("Moon Sign", _pData!['moon_sign'], Icons.dark_mode),
              _buildPanchangCard("Yoga", "Siddhi (Mock)", Icons.self_improvement),
            ],
          ),
        ] else const Center(child: CircularProgressIndicator()),
        const SizedBox(height: 40),
        const Text("Auspicious Timings", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Color(0xFFFFD700))),
        const SizedBox(height: 15),
        _buildTimingRow("Abhijit Muhurat", "11:45 AM - 12:30 PM", Colors.green, Icons.check_circle),
        _buildTimingRow("Brahma Muhurta", "04:30 AM - 05:18 AM", Colors.blueAccent, Icons.wb_twilight),
        const SizedBox(height: 25),
        const Text("Inauspicious Timings", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.redAccent)),
        const SizedBox(height: 15),
        _buildTimingRow("Rahu Kaal", "04:30 PM - 06:00 PM", Colors.redAccent, Icons.warning),
        _buildTimingRow("Yama Gandam", "12:00 PM - 01:30 PM", Colors.orangeAccent, Icons.timer),
      ]
    );
  }

  Widget _buildPanchangCard(String title, String val, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: const Color(0xFF1E1A3C),
        borderRadius: BorderRadius.circular(15),
        border: Border.all(color: Colors.white12)
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: const Color(0xFFFFD700), size: 24),
          const Spacer(),
          Text(title.toUpperCase(), style: const TextStyle(color: Colors.white54, fontSize: 10, letterSpacing: 1)),
          const SizedBox(height: 2),
          Text(val, style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
        ],
      )
    );
  }

  Widget _buildTimingRow(String title, String timing, Color color, IconData icon) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(color: const Color(0xFF1E1A3C), borderRadius: BorderRadius.circular(12)),
      child: Row(
        children: [
          Icon(icon, color: color, size: 20),
          const SizedBox(width: 15),
          Text(title, style: const TextStyle(color: Colors.white, fontSize: 16)),
          const Spacer(),
          Text(timing, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}

// --- PALMISTRY TAB ---
class PalmistryTab extends StatefulWidget {
  const PalmistryTab({super.key});
  @override
  State<PalmistryTab> createState() => _PalmistryTabState();
}

class _PalmistryTabState extends State<PalmistryTab> {
  final ImagePicker _picker = ImagePicker();
  XFile? _image;
  String? _prediction;
  bool _isLoading = false;

  Future<void> _pickImage() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      setState(() {
        _image = image;
        _prediction = null;
      });
    }
  }

  Future<void> _analyzePalm() async {
    if (_image == null) return;
    setState(() => _isLoading = true);
    
    try {
      final bytes = await _image!.readAsBytes();
      var request = http.MultipartRequest('POST', Uri.parse('$apiUrl/predict-palm'));
      request.files.add(http.MultipartFile.fromBytes('file', bytes, filename: _image!.name));
      
      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _prediction = data['prediction'];
        });
      } else {
        setState(() {
          _prediction = "Error connecting to AI Palm Reader. Status: ${response.statusCode}";
        });
      }
    } catch(e) {
      setState(() {
        _prediction = "Network error occurred.";
      });
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          const Text("AI Palmistry", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
          const SizedBox(height: 10),
          const Text("Upload a clear picture of your right palm to get an instant Samudrika Shastra reading from the LLM Vision model.", 
            textAlign: TextAlign.center, style: TextStyle(color: Colors.white54)),
          const SizedBox(height: 30),
          GestureDetector(
            onTap: _pickImage,
            child: Container(
              height: 200, width: 250,
              decoration: BoxDecoration(
                color: const Color(0xFF1E1A3C),
                borderRadius: BorderRadius.circular(15),
                border: Border.all(color: const Color(0xFFFFD700), width: 1, style: BorderStyle.solid)
              ),
              child: _image == null 
                  ? Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: const [
                        Icon(Icons.camera_alt, size: 50, color: Color(0xFFFFD700)),
                        SizedBox(height: 10),
                        Text("Tap to upload Palm Image", style: TextStyle(color: Colors.white70))
                      ],
                    )
                  : const Center(child: Icon(Icons.check_circle, size: 60, color: Colors.green)),
            ),
          ),
          const SizedBox(height: 30),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFFFD700),
              padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 15),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30))
            ),
            onPressed: (_image != null && !_isLoading) ? _analyzePalm : null,
            icon: _isLoading ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2)) : const Icon(Icons.auto_awesome, color: Colors.black),
            label: Text(_isLoading ? "ANALYZING PALM..." : "PREDICT MY FUTURE", style: const TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
          ),
          if (_prediction != null) ...[
            const SizedBox(height: 40),
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: const Color(0xFF1E1A3C),
                borderRadius: BorderRadius.circular(15),
                border: Border.all(color: const Color(0x33FFD700))
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("Your Reading:", style: TextStyle(color: Color(0xFFFFD700), fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 10),
                  Text(_prediction!, style: const TextStyle(color: Colors.white, height: 1.5)),
                ],
              ),
            )
          ]
        ],
      ),
    );
  }
}

// --- AI ASTROLOGER CHAT ---
class AIAstrologerChat extends StatefulWidget {
  final Map<String, dynamic>? Function() getChart;
  const AIAstrologerChat({super.key, required this.getChart});
  @override
  State<AIAstrologerChat> createState() => _AIAstrologerChatState();
}

class _AIAstrologerChatState extends State<AIAstrologerChat> {
  final TextEditingController _msgCtrl = TextEditingController();
  final List<Map<String, dynamic>> _messages = [];
  bool _isTyping = false;

  void _sendMessage() async {
    if (_msgCtrl.text.trim().isEmpty) return;
    String userText = _msgCtrl.text.trim();
    setState(() {
      _messages.add({"isUser": true, "text": userText});
      _msgCtrl.clear();
      _isTyping = true;
    });

    final chart = widget.getChart() ?? {};

    try {
      final res = await http.post(
          Uri.parse('$apiUrl/api/v1/chat'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            "message": userText,
            "user_id": "user123",
            "chart_context": chart
          })
      );
      if(mounted && res.statusCode == 200) {
        final data = jsonDecode(res.body);
        setState(() {
          _messages.add({"isUser": false, "text": data['reply']});
        });
      }
    } catch(e) {
      setState(() => _messages.add({"isUser": false, "text": "Error connecting to AI Sage."}));
    } finally {
      if(mounted) setState(() => _isTyping = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
          decoration: const BoxDecoration(border: Border(bottom: BorderSide(color: Color(0x33FFD700)))),
          child: Row(
            children: const [
              CircleAvatar(backgroundColor: Color(0x22FFD700), child: Icon(Icons.psychology, color: Color(0xFFFFD700))),
              SizedBox(width: 15),
              Text("Vedic AI Sage", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
            ],
          ),
        ),
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(20),
            itemCount: _messages.length + (_isTyping ? 1 : 0),
            itemBuilder: (context, index) {
              if (index == _messages.length && _isTyping) {
                return const Align(alignment: Alignment.centerLeft, child: Text("Consulting...", style: TextStyle(color: Colors.white54, fontStyle: FontStyle.italic)));
              }
              final msg = _messages[index];
              return Align(
                alignment: msg["isUser"] ? Alignment.centerRight : Alignment.centerLeft,
                child: Container(
                  margin: const EdgeInsets.symmetric(vertical: 8),
                  padding: const EdgeInsets.all(15),
                  constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
                  decoration: BoxDecoration(
                    color: msg["isUser"] ? const Color(0x44FFD700) : const Color(0xFF1E1A3C),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(msg["text"], style: TextStyle(color: msg["isUser"] ? Colors.white : Colors.white70)),
                ),
              );
            },
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(15),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _msgCtrl,
                  style: const TextStyle(color: Colors.white),
                  decoration: InputDecoration(
                    hintText: "Ask your AI Sage...",
                    filled: true,
                    fillColor: const Color(0xFF1E1A3C),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(30), borderSide: BorderSide.none),
                  ),
                  onSubmitted: (_) => _sendMessage(),
                ),
              ),
              IconButton(onPressed: _sendMessage, icon: const Icon(Icons.send, color: Color(0xFFFFD700)))
            ],
          ),
        )
      ],
    );
  }
}
