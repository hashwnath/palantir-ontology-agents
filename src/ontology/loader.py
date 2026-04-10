"""Sample data loader for Taiwan Strait supply chain disruption scenario.

Populates an OntologyStore with ~50 realistic entities and ~100 relationships
spanning semiconductor manufacturing, shipping logistics, military deployments,
and geopolitical events in the Western Pacific region.
"""

from __future__ import annotations

from src.ontology.schema import (
    Organization, Person, Location, Event, Asset, Threat,
    Relationship, RelationshipType,
)
from src.ontology.store import OntologyStore


def load_sample_data() -> OntologyStore:
    """Load realistic Taiwan Strait scenario data into an OntologyStore."""
    store = OntologyStore()

    # =========================================================================
    # ORGANIZATIONS
    # =========================================================================
    orgs = [
        Organization(id="tsmc", name="TSMC", description="Taiwan Semiconductor Manufacturing Company - world's largest contract chipmaker",
                     org_type="corporation", country="Taiwan", sector="semiconductor", revenue_usd=75_000_000_000,
                     tags=["critical_infrastructure", "semiconductor"]),
        Organization(id="asml", name="ASML", description="Dutch semiconductor equipment manufacturer - sole supplier of EUV lithography",
                     org_type="corporation", country="Netherlands", sector="semiconductor_equipment", revenue_usd=28_000_000_000,
                     tags=["semiconductor", "critical_supplier"]),
        Organization(id="apple", name="Apple Inc.", description="Major TSMC customer - A-series and M-series chip fabrication",
                     org_type="corporation", country="USA", sector="technology", revenue_usd=394_000_000_000,
                     tags=["tsmc_customer"]),
        Organization(id="nvidia", name="NVIDIA", description="GPU design company - relies on TSMC for advanced node fabrication",
                     org_type="corporation", country="USA", sector="semiconductor", revenue_usd=61_000_000_000,
                     tags=["tsmc_customer"]),
        Organization(id="uspacflt", name="US Pacific Fleet", description="United States Pacific Fleet - primary naval force in Western Pacific",
                     org_type="military", country="USA", sector="defense",
                     tags=["military", "indo_pacific"]),
        Organization(id="pla_navy", name="PLA Navy", description="People's Liberation Army Navy - China's naval force",
                     org_type="military", country="China", sector="defense",
                     tags=["military", "china"]),
        Organization(id="pla_eastern", name="PLA Eastern Theater Command", description="Chinese military command responsible for Taiwan contingency",
                     org_type="military", country="China", sector="defense",
                     tags=["military", "china"]),
        Organization(id="maersk", name="Maersk", description="Danish shipping and logistics conglomerate",
                     org_type="corporation", country="Denmark", sector="shipping", revenue_usd=51_000_000_000,
                     tags=["shipping", "logistics"]),
        Organization(id="evergreen", name="Evergreen Marine", description="Taiwanese container shipping company",
                     org_type="corporation", country="Taiwan", sector="shipping", revenue_usd=16_000_000_000,
                     tags=["shipping", "taiwan"]),
        Organization(id="cosco", name="COSCO Shipping", description="Chinese state-owned shipping conglomerate",
                     org_type="corporation", country="China", sector="shipping", revenue_usd=37_000_000_000,
                     tags=["shipping", "china", "state_owned"]),
        Organization(id="taiwan_mod", name="Taiwan Ministry of Defense", description="Republic of China Ministry of National Defense",
                     org_type="government", country="Taiwan", sector="defense",
                     tags=["government", "taiwan", "defense"]),
        Organization(id="usdod", name="US Department of Defense", description="United States Department of Defense",
                     org_type="government", country="USA", sector="defense",
                     tags=["government", "usa", "defense"]),
        Organization(id="samsung_semi", name="Samsung Semiconductor", description="Samsung's semiconductor division - TSMC competitor",
                     org_type="corporation", country="South Korea", sector="semiconductor", revenue_usd=63_000_000_000,
                     tags=["semiconductor", "alternative_supplier"]),
        Organization(id="intel_foundry", name="Intel Foundry Services", description="Intel's contract manufacturing division",
                     org_type="corporation", country="USA", sector="semiconductor", revenue_usd=1_000_000_000,
                     tags=["semiconductor", "alternative_supplier"]),
        Organization(id="yang_ming", name="Yang Ming Marine", description="Taiwanese shipping line operating in the Pacific",
                     org_type="corporation", country="Taiwan", sector="shipping", revenue_usd=8_000_000_000,
                     tags=["shipping", "taiwan"]),
        Organization(id="jtf_7", name="Joint Task Force 7", description="US military joint task force for Western Pacific operations",
                     org_type="military", country="USA", sector="defense",
                     tags=["military", "usa"]),
    ]

    # =========================================================================
    # PERSONS
    # =========================================================================
    persons = [
        Person(id="cc_wei", name="C.C. Wei", description="CEO of TSMC",
               role="CEO", nationality="Taiwanese", affiliation="TSMC"),
        Person(id="adm_paparo", name="ADM Samuel Paparo", description="Commander, US Indo-Pacific Command",
               role="INDOPACOM Commander", nationality="American", affiliation="US Indo-Pacific Command"),
        Person(id="dong_jun", name="Dong Jun", description="Chinese Minister of National Defense",
               role="Defense Minister", nationality="Chinese", affiliation="PLA"),
        Person(id="lai_ching_te", name="Lai Ching-te", description="President of Taiwan",
               role="President", nationality="Taiwanese", affiliation="Taiwan Government"),
    ]

    # =========================================================================
    # LOCATIONS
    # =========================================================================
    locations = [
        Location(id="taiwan_strait", name="Taiwan Strait", description="Strategic waterway between Taiwan and mainland China, 110 miles wide",
                 latitude=24.5, longitude=119.5, location_type="strait", country="International"),
        Location(id="hsinchu", name="Hsinchu Science Park", description="TSMC primary fabrication complex - produces >90% of advanced chips",
                 latitude=24.8, longitude=120.98, location_type="industrial_park", country="Taiwan"),
        Location(id="kaohsiung_port", name="Port of Kaohsiung", description="Taiwan's largest port, handles 60% of container traffic",
                 latitude=22.61, longitude=120.27, location_type="port", country="Taiwan"),
        Location(id="keelung_port", name="Port of Keelung", description="Major Taiwan northern port near Taipei",
                 latitude=25.13, longitude=121.74, location_type="port", country="Taiwan"),
        Location(id="shanghai_port", name="Port of Shanghai", description="World's busiest container port",
                 latitude=31.23, longitude=121.47, location_type="port", country="China"),
        Location(id="yokosuka", name="Yokosuka Naval Base", description="US Navy 7th Fleet headquarters in Japan",
                 latitude=35.28, longitude=139.67, location_type="base", country="Japan"),
        Location(id="guam", name="Naval Base Guam", description="Strategic US military base in the Western Pacific",
                 latitude=13.44, longitude=144.79, location_type="base", country="USA"),
        Location(id="fuzhou", name="Fuzhou", description="PLA Eastern Theater Command naval facilities opposite Taiwan",
                 latitude=26.07, longitude=119.30, location_type="base", country="China"),
        Location(id="xiamen", name="Xiamen", description="Chinese port city facing Taiwan across the strait",
                 latitude=24.48, longitude=118.09, location_type="port", country="China"),
        Location(id="bashi_channel", name="Bashi Channel", description="Critical waterway south of Taiwan connecting Pacific to South China Sea",
                 latitude=21.0, longitude=121.5, location_type="strait", country="International"),
        Location(id="subic_bay", name="Subic Bay", description="Former US naval base, now Philippine freeport with military access agreement",
                 latitude=14.79, longitude=120.28, location_type="base", country="Philippines"),
        Location(id="tainan_fab", name="TSMC Tainan Fab 18", description="TSMC 5nm/3nm fabrication facility in southern Taiwan",
                 latitude=23.0, longitude=120.23, location_type="facility", country="Taiwan"),
    ]

    # =========================================================================
    # EVENTS
    # =========================================================================
    events = [
        Event(id="pla_exercise_2026", name="PLA Joint Sword-2026A", description="Large-scale PLA military exercises around Taiwan simulating blockade operations",
              event_type="military_exercise", start_date="2026-03-15", end_date="2026-03-22", severity="critical",
              tags=["military", "china", "taiwan"]),
        Event(id="shipping_disruption", name="Taiwan Strait Shipping Disruption", description="Commercial shipping rerouting due to PLA exercise zones, adding 3-5 days transit",
              event_type="trade_disruption", start_date="2026-03-16", end_date="2026-03-25", severity="high",
              tags=["shipping", "trade", "supply_chain"]),
        Event(id="chip_shortage_alert", name="Semiconductor Supply Alert", description="TSMC warns of potential production delays due to regional security concerns",
              event_type="trade_disruption", start_date="2026-03-18", severity="high",
              tags=["semiconductor", "supply_chain"]),
        Event(id="us_carrier_deploy", name="USS Ronald Reagan CSG Deployment", description="US carrier strike group surges to Western Pacific in response to PLA exercises",
              event_type="military_exercise", start_date="2026-03-17", severity="high",
              tags=["military", "usa", "deployment"]),
        Event(id="asml_export_pause", name="ASML Export License Review", description="Netherlands reviews EUV equipment export licenses to Taiwan amid tensions",
              event_type="diplomatic", start_date="2026-03-19", severity="medium",
              tags=["semiconductor", "export_control"]),
        Event(id="cyber_incident", name="Taiwan Infrastructure Cyber Attack", description="Suspected state-sponsored cyber attack on Taiwan port management systems",
              event_type="trade_disruption", start_date="2026-03-20", severity="high",
              tags=["cyber", "taiwan", "infrastructure"]),
    ]

    # =========================================================================
    # ASSETS
    # =========================================================================
    assets = [
        Asset(id="uss_reagan", name="USS Ronald Reagan (CVN-76)", description="Nimitz-class aircraft carrier",
              asset_type="vessel", operator="US Navy", status="deployed",
              tags=["carrier", "7th_fleet"]),
        Asset(id="uss_mustin", name="USS Mustin (DDG-89)", description="Arleigh Burke-class guided-missile destroyer",
              asset_type="vessel", operator="US Navy", status="deployed",
              tags=["destroyer", "7th_fleet"]),
        Asset(id="euv_scanner", name="ASML TWINSCAN NXE:3800E", description="Latest generation EUV lithography scanner - essential for sub-5nm chips",
              asset_type="technology", operator="ASML", status="active",
              tags=["semiconductor", "critical_equipment"]),
        Asset(id="tsmc_3nm_line", name="TSMC N3E Production Line", description="3nm enhanced process production capability at Tainan Fab 18",
              asset_type="facility", operator="TSMC", status="active",
              tags=["semiconductor", "production"]),
        Asset(id="ever_given_class", name="Ever Ace", description="Evergreen 24,000 TEU container vessel operating in Asia-Pacific",
              asset_type="vessel", operator="Evergreen Marine", status="active",
              tags=["container_ship", "shipping"]),
        Asset(id="liaoning", name="Liaoning (CV-16)", description="PLA Navy aircraft carrier",
              asset_type="vessel", operator="PLA Navy", status="deployed",
              tags=["carrier", "pla_navy"]),
        Asset(id="shandong", name="Shandong (CV-17)", description="PLA Navy Type 002 aircraft carrier",
              asset_type="vessel", operator="PLA Navy", status="deployed",
              tags=["carrier", "pla_navy"]),
    ]

    # =========================================================================
    # THREATS
    # =========================================================================
    threats = [
        Threat(id="strait_blockade", name="Taiwan Strait Blockade Scenario", description="PLA enforces naval/air blockade of Taiwan, cutting all commercial shipping",
               threat_type="military", severity="critical", likelihood=0.15,
               impact_description="Complete disruption of semiconductor supply chain, 60%+ of global advanced chip production offline"),
        Threat(id="gray_zone_ops", name="Gray Zone Maritime Operations", description="PLA increases coast guard and maritime militia presence, harassing commercial shipping",
               threat_type="hybrid", severity="high", likelihood=0.45,
               impact_description="Shipping delays of 5-15 days, insurance rate spikes, port congestion"),
        Threat(id="cyber_supply_chain", name="Supply Chain Cyber Attack", description="State-sponsored cyber operations targeting port systems and semiconductor logistics",
               threat_type="cyber", severity="high", likelihood=0.35,
               impact_description="Disruption to port operations, potential production delays at TSMC"),
        Threat(id="export_controls", name="Escalating Export Controls", description="Expanded export controls on semiconductor equipment and IP to/from Taiwan",
               threat_type="economic", severity="medium", likelihood=0.55,
               impact_description="Constrained access to EUV equipment, slower technology advancement"),
    ]

    # Add all entities
    for entity_list in [orgs, persons, locations, events, assets, threats]:
        for entity in entity_list:
            store.add_entity(entity)

    # =========================================================================
    # RELATIONSHIPS (~100)
    # =========================================================================
    rels = [
        # --- TSMC relationships ---
        Relationship(id="r01", source_id="tsmc", target_id="hsinchu", relationship_type=RelationshipType.HEADQUARTERED_IN,
                     description="TSMC headquartered in Hsinchu Science Park"),
        Relationship(id="r02", source_id="tsmc", target_id="tainan_fab", relationship_type=RelationshipType.OPERATES_IN,
                     description="TSMC operates 3nm fabrication in Tainan"),
        Relationship(id="r03", source_id="tsmc", target_id="kaohsiung_port", relationship_type=RelationshipType.SHIPS_THROUGH,
                     description="TSMC ships finished wafers through Kaohsiung"),
        Relationship(id="r04", source_id="tsmc", target_id="keelung_port", relationship_type=RelationshipType.SHIPS_THROUGH,
                     description="TSMC receives materials through Keelung"),
        Relationship(id="r05", source_id="tsmc", target_id="taiwan_strait", relationship_type=RelationshipType.DEPENDS_ON,
                     description="TSMC supply chain depends on strait passage", weight=0.95),
        Relationship(id="r06", source_id="tsmc", target_id="asml", relationship_type=RelationshipType.DEPENDS_ON,
                     description="TSMC depends on ASML for EUV lithography equipment", weight=0.99),
        Relationship(id="r07", source_id="tsmc", target_id="cc_wei", relationship_type=RelationshipType.EMPLOYS,
                     description="C.C. Wei leads TSMC as CEO"),
        Relationship(id="r08", source_id="tsmc_3nm_line", target_id="tsmc", relationship_type=RelationshipType.RELATED_TO,
                     description="TSMC 3nm line is core production asset"),
        Relationship(id="r09", source_id="tsmc_3nm_line", target_id="tainan_fab", relationship_type=RelationshipType.LOCATED_IN,
                     description="3nm line located at Tainan Fab 18"),
        Relationship(id="r10", source_id="euv_scanner", target_id="tsmc_3nm_line", relationship_type=RelationshipType.RELATED_TO,
                     description="EUV scanners critical for 3nm production"),

        # --- Customer dependencies on TSMC ---
        Relationship(id="r11", source_id="apple", target_id="tsmc", relationship_type=RelationshipType.DEPENDS_ON,
                     description="Apple relies on TSMC for A-series and M-series chips", weight=0.95),
        Relationship(id="r12", source_id="nvidia", target_id="tsmc", relationship_type=RelationshipType.DEPENDS_ON,
                     description="NVIDIA relies on TSMC for GPU fabrication", weight=0.90),
        Relationship(id="r13", source_id="tsmc", target_id="apple", relationship_type=RelationshipType.SUPPLIES_TO,
                     description="TSMC supplies advanced chips to Apple"),
        Relationship(id="r14", source_id="tsmc", target_id="nvidia", relationship_type=RelationshipType.SUPPLIES_TO,
                     description="TSMC supplies GPU dies to NVIDIA"),

        # --- ASML supply chain ---
        Relationship(id="r15", source_id="asml", target_id="tsmc", relationship_type=RelationshipType.SUPPLIES,
                     description="ASML supplies EUV lithography equipment to TSMC"),
        Relationship(id="r16", source_id="asml", target_id="samsung_semi", relationship_type=RelationshipType.SUPPLIES,
                     description="ASML supplies EUV equipment to Samsung"),
        Relationship(id="r17", source_id="euv_scanner", target_id="asml", relationship_type=RelationshipType.RELATED_TO,
                     description="EUV scanner is ASML flagship product"),
        Relationship(id="r18", source_id="asml_export_pause", target_id="asml", relationship_type=RelationshipType.RELATED_TO,
                     description="Export review directly affects ASML"),
        Relationship(id="r19", source_id="asml_export_pause", target_id="tsmc", relationship_type=RelationshipType.THREATENS,
                     description="Export pause threatens TSMC equipment access"),

        # --- Shipping relationships ---
        Relationship(id="r20", source_id="maersk", target_id="taiwan_strait", relationship_type=RelationshipType.TRANSITS,
                     description="Maersk container vessels transit Taiwan Strait"),
        Relationship(id="r21", source_id="evergreen", target_id="taiwan_strait", relationship_type=RelationshipType.TRANSITS,
                     description="Evergreen vessels regularly transit Taiwan Strait"),
        Relationship(id="r22", source_id="cosco", target_id="taiwan_strait", relationship_type=RelationshipType.TRANSITS,
                     description="COSCO vessels transit Taiwan Strait"),
        Relationship(id="r23", source_id="yang_ming", target_id="taiwan_strait", relationship_type=RelationshipType.TRANSITS,
                     description="Yang Ming vessels transit Taiwan Strait"),
        Relationship(id="r24", source_id="evergreen", target_id="kaohsiung_port", relationship_type=RelationshipType.OPERATES_IN,
                     description="Evergreen operates from Kaohsiung"),
        Relationship(id="r25", source_id="maersk", target_id="shanghai_port", relationship_type=RelationshipType.OPERATES_IN,
                     description="Maersk operates major hub in Shanghai"),
        Relationship(id="r26", source_id="cosco", target_id="shanghai_port", relationship_type=RelationshipType.HEADQUARTERED_IN,
                     description="COSCO headquartered near Shanghai"),
        Relationship(id="r27", source_id="ever_given_class", target_id="evergreen", relationship_type=RelationshipType.RELATED_TO,
                     description="Ever Ace operated by Evergreen Marine"),
        Relationship(id="r28", source_id="ever_given_class", target_id="taiwan_strait", relationship_type=RelationshipType.TRANSITS,
                     description="Ever Ace transits Taiwan Strait on Asia-Europe route"),
        Relationship(id="r29", source_id="yang_ming", target_id="kaohsiung_port", relationship_type=RelationshipType.OPERATES_IN,
                     description="Yang Ming operates from Kaohsiung"),
        Relationship(id="r30", source_id="shipping_disruption", target_id="taiwan_strait", relationship_type=RelationshipType.LOCATED_IN,
                     description="Shipping disruption centered on Taiwan Strait"),

        # --- US Military ---
        Relationship(id="r31", source_id="uspacflt", target_id="yokosuka", relationship_type=RelationshipType.HEADQUARTERED_IN,
                     description="Pacific Fleet 7th Fleet HQ at Yokosuka"),
        Relationship(id="r32", source_id="uss_reagan", target_id="uspacflt", relationship_type=RelationshipType.RELATED_TO,
                     description="USS Reagan assigned to Pacific Fleet"),
        Relationship(id="r33", source_id="uss_mustin", target_id="uspacflt", relationship_type=RelationshipType.RELATED_TO,
                     description="USS Mustin part of Pacific Fleet"),
        Relationship(id="r34", source_id="uss_reagan", target_id="taiwan_strait", relationship_type=RelationshipType.DEPLOYED_AT,
                     description="USS Reagan deployed near Taiwan Strait"),
        Relationship(id="r35", source_id="uss_mustin", target_id="taiwan_strait", relationship_type=RelationshipType.DEPLOYED_AT,
                     description="USS Mustin conducting freedom of navigation"),
        Relationship(id="r36", source_id="us_carrier_deploy", target_id="uss_reagan", relationship_type=RelationshipType.RELATED_TO,
                     description="Carrier deployment event involves USS Reagan"),
        Relationship(id="r37", source_id="adm_paparo", target_id="uspacflt", relationship_type=RelationshipType.COMMANDS,
                     description="ADM Paparo commands Indo-Pacific forces"),
        Relationship(id="r38", source_id="usdod", target_id="uspacflt", relationship_type=RelationshipType.COMMANDS,
                     description="DoD oversees Pacific Fleet"),
        Relationship(id="r39", source_id="usdod", target_id="jtf_7", relationship_type=RelationshipType.COMMANDS,
                     description="DoD directs JTF-7 operations"),
        Relationship(id="r40", source_id="jtf_7", target_id="guam", relationship_type=RelationshipType.DEPLOYED_AT,
                     description="JTF-7 operates from Guam"),
        Relationship(id="r41", source_id="uspacflt", target_id="subic_bay", relationship_type=RelationshipType.OPERATES_IN,
                     description="Pacific Fleet has access to Subic Bay"),

        # --- PLA Military ---
        Relationship(id="r42", source_id="pla_navy", target_id="pla_eastern", relationship_type=RelationshipType.RELATED_TO,
                     description="PLA Navy supports Eastern Theater operations"),
        Relationship(id="r43", source_id="pla_eastern", target_id="fuzhou", relationship_type=RelationshipType.HEADQUARTERED_IN,
                     description="Eastern Theater Command facilities near Fuzhou"),
        Relationship(id="r44", source_id="liaoning", target_id="pla_navy", relationship_type=RelationshipType.RELATED_TO,
                     description="Liaoning is PLA Navy carrier"),
        Relationship(id="r45", source_id="shandong", target_id="pla_navy", relationship_type=RelationshipType.RELATED_TO,
                     description="Shandong is PLA Navy carrier"),
        Relationship(id="r46", source_id="liaoning", target_id="taiwan_strait", relationship_type=RelationshipType.DEPLOYED_AT,
                     description="Liaoning deployed east of Taiwan during exercises"),
        Relationship(id="r47", source_id="shandong", target_id="bashi_channel", relationship_type=RelationshipType.DEPLOYED_AT,
                     description="Shandong positioned near Bashi Channel"),
        Relationship(id="r48", source_id="dong_jun", target_id="pla_navy", relationship_type=RelationshipType.COMMANDS,
                     description="Defense Minister oversees PLA Navy"),
        Relationship(id="r49", source_id="pla_exercise_2026", target_id="pla_eastern", relationship_type=RelationshipType.RELATED_TO,
                     description="Exercise conducted by Eastern Theater Command"),
        Relationship(id="r50", source_id="pla_exercise_2026", target_id="taiwan_strait", relationship_type=RelationshipType.LOCATED_IN,
                     description="Exercise zones in Taiwan Strait"),

        # --- Taiwan defense ---
        Relationship(id="r51", source_id="taiwan_mod", target_id="lai_ching_te", relationship_type=RelationshipType.RELATED_TO,
                     description="MoD reports to President Lai"),
        Relationship(id="r52", source_id="taiwan_mod", target_id="taiwan_strait", relationship_type=RelationshipType.MONITORS,
                     description="Taiwan MoD monitors strait activities"),
        Relationship(id="r53", source_id="usdod", target_id="taiwan_mod", relationship_type=RelationshipType.ALLIES_WITH,
                     description="US-Taiwan defense cooperation"),

        # --- Threat relationships ---
        Relationship(id="r54", source_id="strait_blockade", target_id="taiwan_strait", relationship_type=RelationshipType.LOCATED_IN,
                     description="Blockade threat centered on strait"),
        Relationship(id="r55", source_id="strait_blockade", target_id="tsmc", relationship_type=RelationshipType.THREATENS,
                     description="Blockade would cut TSMC supply chain"),
        Relationship(id="r56", source_id="strait_blockade", target_id="kaohsiung_port", relationship_type=RelationshipType.THREATENS,
                     description="Blockade would shut Kaohsiung port"),
        Relationship(id="r57", source_id="strait_blockade", target_id="maersk", relationship_type=RelationshipType.THREATENS,
                     description="Blockade disrupts Maersk operations"),
        Relationship(id="r58", source_id="strait_blockade", target_id="evergreen", relationship_type=RelationshipType.THREATENS,
                     description="Blockade threatens Evergreen operations"),
        Relationship(id="r59", source_id="gray_zone_ops", target_id="taiwan_strait", relationship_type=RelationshipType.LOCATED_IN,
                     description="Gray zone operations in strait area"),
        Relationship(id="r60", source_id="gray_zone_ops", target_id="evergreen", relationship_type=RelationshipType.THREATENS,
                     description="Gray zone ops harass Taiwanese shipping"),
        Relationship(id="r61", source_id="gray_zone_ops", target_id="yang_ming", relationship_type=RelationshipType.THREATENS,
                     description="Gray zone ops affect Yang Ming"),
        Relationship(id="r62", source_id="cyber_supply_chain", target_id="kaohsiung_port", relationship_type=RelationshipType.THREATENS,
                     description="Cyber threat to port systems"),
        Relationship(id="r63", source_id="cyber_supply_chain", target_id="tsmc", relationship_type=RelationshipType.THREATENS,
                     description="Cyber threat to TSMC logistics"),
        Relationship(id="r64", source_id="cyber_incident", target_id="cyber_supply_chain", relationship_type=RelationshipType.RELATED_TO,
                     description="Actual cyber incident matches threat profile"),
        Relationship(id="r65", source_id="export_controls", target_id="asml", relationship_type=RelationshipType.THREATENS,
                     description="Export controls affect ASML shipments"),
        Relationship(id="r66", source_id="export_controls", target_id="tsmc", relationship_type=RelationshipType.THREATENS,
                     description="Export controls limit TSMC equipment access"),

        # --- Event cascades ---
        Relationship(id="r67", source_id="pla_exercise_2026", target_id="shipping_disruption", relationship_type=RelationshipType.RELATED_TO,
                     description="PLA exercise caused shipping disruption"),
        Relationship(id="r68", source_id="shipping_disruption", target_id="chip_shortage_alert", relationship_type=RelationshipType.RELATED_TO,
                     description="Shipping disruption triggered chip supply alert"),
        Relationship(id="r69", source_id="pla_exercise_2026", target_id="us_carrier_deploy", relationship_type=RelationshipType.RELATED_TO,
                     description="PLA exercise prompted US carrier deployment"),
        Relationship(id="r70", source_id="chip_shortage_alert", target_id="tsmc", relationship_type=RelationshipType.RELATED_TO,
                     description="TSMC issued the supply alert"),
        Relationship(id="r71", source_id="shipping_disruption", target_id="maersk", relationship_type=RelationshipType.THREATENS,
                     description="Disruption forces Maersk rerouting"),
        Relationship(id="r72", source_id="shipping_disruption", target_id="evergreen", relationship_type=RelationshipType.THREATENS,
                     description="Disruption severely impacts Evergreen"),
        Relationship(id="r73", source_id="cyber_incident", target_id="kaohsiung_port", relationship_type=RelationshipType.THREATENS,
                     description="Cyber attack hit Kaohsiung port systems"),

        # --- Alternative supplier relationships ---
        Relationship(id="r74", source_id="samsung_semi", target_id="apple", relationship_type=RelationshipType.SUPPLIES_TO,
                     description="Samsung as backup supplier to Apple"),
        Relationship(id="r75", source_id="intel_foundry", target_id="usdod", relationship_type=RelationshipType.SUPPLIES_TO,
                     description="Intel Foundry for DoD chip needs"),
        Relationship(id="r76", source_id="samsung_semi", target_id="nvidia", relationship_type=RelationshipType.SUPPLIES_TO,
                     description="Samsung as potential NVIDIA backup"),
        Relationship(id="r77", source_id="tsmc", target_id="samsung_semi", relationship_type=RelationshipType.COMPETES_WITH,
                     description="TSMC and Samsung compete in foundry"),
        Relationship(id="r78", source_id="tsmc", target_id="intel_foundry", relationship_type=RelationshipType.COMPETES_WITH,
                     description="TSMC and Intel compete in foundry"),

        # --- Geographic relationships ---
        Relationship(id="r79", source_id="hsinchu", target_id="taiwan_strait", relationship_type=RelationshipType.RELATED_TO,
                     description="Hsinchu on Taiwan's west coast near strait"),
        Relationship(id="r80", source_id="kaohsiung_port", target_id="taiwan_strait", relationship_type=RelationshipType.RELATED_TO,
                     description="Kaohsiung port opens to Taiwan Strait"),
        Relationship(id="r81", source_id="fuzhou", target_id="taiwan_strait", relationship_type=RelationshipType.RELATED_TO,
                     description="Fuzhou faces Taiwan across the strait"),
        Relationship(id="r82", source_id="xiamen", target_id="taiwan_strait", relationship_type=RelationshipType.RELATED_TO,
                     description="Xiamen at narrowest point of strait"),
        Relationship(id="r83", source_id="bashi_channel", target_id="taiwan_strait", relationship_type=RelationshipType.RELATED_TO,
                     description="Bashi Channel is southern approach to strait"),

        # --- PLA monitoring/threat to US forces ---
        Relationship(id="r84", source_id="pla_eastern", target_id="uss_reagan", relationship_type=RelationshipType.MONITORS,
                     description="PLA Eastern Theater tracks US carrier"),
        Relationship(id="r85", source_id="pla_eastern", target_id="taiwan_strait", relationship_type=RelationshipType.MONITORS,
                     description="PLA monitors all strait activity"),
        Relationship(id="r86", source_id="uspacflt", target_id="pla_eastern", relationship_type=RelationshipType.MONITORS,
                     description="US Pacific Fleet monitors PLA Eastern"),
        Relationship(id="r87", source_id="uspacflt", target_id="taiwan_strait", relationship_type=RelationshipType.MONITORS,
                     description="US monitors Taiwan Strait"),

        # --- Supply chain dependencies ---
        Relationship(id="r88", source_id="apple", target_id="taiwan_strait", relationship_type=RelationshipType.DEPENDS_ON,
                     description="Apple supply chain depends on strait passage", weight=0.85),
        Relationship(id="r89", source_id="nvidia", target_id="taiwan_strait", relationship_type=RelationshipType.DEPENDS_ON,
                     description="NVIDIA supply chain depends on strait passage", weight=0.80),
        Relationship(id="r90", source_id="usdod", target_id="tsmc", relationship_type=RelationshipType.DEPENDS_ON,
                     description="DoD defense systems depend on TSMC chips", weight=0.60),

        # --- Port-shipping dependencies ---
        Relationship(id="r91", source_id="kaohsiung_port", target_id="taiwan_strait", relationship_type=RelationshipType.DEPENDS_ON,
                     description="Kaohsiung depends on strait for shipping"),
        Relationship(id="r92", source_id="keelung_port", target_id="taiwan_strait", relationship_type=RelationshipType.DEPENDS_ON,
                     description="Keelung depends on open strait"),
        Relationship(id="r93", source_id="evergreen", target_id="kaohsiung_port", relationship_type=RelationshipType.DEPENDS_ON,
                     description="Evergreen depends on Kaohsiung hub"),
        Relationship(id="r94", source_id="tsmc", target_id="evergreen", relationship_type=RelationshipType.DEPENDS_ON,
                     description="TSMC uses Evergreen for shipping"),
        Relationship(id="r95", source_id="tsmc", target_id="maersk", relationship_type=RelationshipType.DEPENDS_ON,
                     description="TSMC uses Maersk for logistics"),

        # --- Additional cross-links ---
        Relationship(id="r96", source_id="pla_exercise_2026", target_id="strait_blockade", relationship_type=RelationshipType.RELATED_TO,
                     description="Exercise rehearses blockade scenario"),
        Relationship(id="r97", source_id="gray_zone_ops", target_id="pla_exercise_2026", relationship_type=RelationshipType.RELATED_TO,
                     description="Gray zone ops escalated during exercise"),
        Relationship(id="r98", source_id="cosco", target_id="pla_navy", relationship_type=RelationshipType.RELATED_TO,
                     description="COSCO state-owned, coordinates with PLA Navy",
                     attributes={"note": "dual-use concern"}),
        Relationship(id="r99", source_id="pla_navy", target_id="xiamen", relationship_type=RelationshipType.OPERATES_IN,
                     description="PLA Navy operates from Xiamen"),
        Relationship(id="r100", source_id="tainan_fab", target_id="kaohsiung_port", relationship_type=RelationshipType.RELATED_TO,
                      description="Tainan fab ships via nearby Kaohsiung"),
    ]

    for rel in rels:
        store.add_relationship(rel)

    return store
