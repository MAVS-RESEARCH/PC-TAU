# LLM1 model results

Intervals are task-context bootstrap CIs under the shared constructed mechanism, never prevalence.

```json
{
  "tracks": {
    "F": {
      "budget_outcomes": 1,
      "deepseek/deepseek-v4-flash": {
        "excess_escalation": {
          "hi": 0.13414634146341464,
          "lo": 0.024390243902439025,
          "mean": 0.07317073170731707
        },
        "f000_governance": {
          "hi": 1.0,
          "lo": 1.0,
          "mean": 1.0
        },
        "f010_governance": {
          "hi": 0.8571428571428571,
          "lo": 0.47619047619047616,
          "mean": 0.6666666666666666
        },
        "finite_fallback_discovery": {
          "hi": 0.7619047619047619,
          "lo": 0.3333333333333333,
          "mean": 0.5714285714285714
        },
        "freeze_adaptation": {
          "hi": 0.6707317073170732,
          "lo": 0.45121951219512196,
          "mean": 0.5609756097560976
        },
        "governance_correct": {
          "hi": 0.7682926829268293,
          "lo": 0.5609756097560976,
          "mean": 0.6707317073170732
        },
        "optimal_route": {
          "hi": 0.0,
          "lo": 0.0,
          "mean": 0.0
        },
        "repair_regret_mean": 1.891304347826087,
        "resolved": 82,
        "route_discovery": {
          "hi": 0.6707317073170732,
          "lo": 0.45121951219512196,
          "mean": 0.5609756097560976
        },
        "unsafe_total": 7
      },
      "episodes": 576,
      "qwen/qwen3.7-flash": {
        "excess_escalation": {
          "hi": 0.0718954248366013,
          "lo": 0.013071895424836602,
          "mean": 0.0392156862745098
        },
        "f000_governance": {
          "hi": 1.0,
          "lo": 1.0,
          "mean": 1.0
        },
        "f010_governance": {
          "hi": 0.5641025641025641,
          "lo": 0.2564102564102564,
          "mean": 0.41025641025641024
        },
        "finite_fallback_discovery": {
          "hi": 0.2564102564102564,
          "lo": 0.02564102564102564,
          "mean": 0.1282051282051282
        },
        "freeze_adaptation": {
          "hi": 0.6143790849673203,
          "lo": 0.45751633986928103,
          "mean": 0.5359477124183006
        },
        "governance_correct": {
          "hi": 0.6013071895424836,
          "lo": 0.43790849673202614,
          "mean": 0.5163398692810458
        },
        "optimal_route": {
          "hi": 0.0,
          "lo": 0.0,
          "mean": 0.0
        },
        "repair_regret_mean": 0.2926829268292683,
        "resolved": 153,
        "route_discovery": {
          "hi": 0.6143790849673203,
          "lo": 0.45751633986928103,
          "mean": 0.5359477124183006
        },
        "unsafe_total": 40
      },
      "transport_outcomes": 221,
      "z-ai/glm-4.7-flash": {
        "excess_escalation": {
          "hi": 0.15966386554621848,
          "lo": 0.05042016806722689,
          "mean": 0.10084033613445378
        },
        "f000_governance": {
          "hi": 0.37037037037037035,
          "lo": 0.07407407407407407,
          "mean": 0.2222222222222222
        },
        "f010_governance": {
          "hi": 0.20689655172413793,
          "lo": 0.0,
          "mean": 0.10344827586206896
        },
        "finite_fallback_discovery": {
          "hi": 0.20689655172413793,
          "lo": 0.0,
          "mean": 0.10344827586206896
        },
        "freeze_adaptation": {
          "hi": 0.6302521008403361,
          "lo": 0.44537815126050423,
          "mean": 0.5462184873949579
        },
        "governance_correct": {
          "hi": 0.3445378151260504,
          "lo": 0.17647058823529413,
          "mean": 0.2605042016806723
        },
        "optimal_route": {
          "hi": 0.0,
          "lo": 0.0,
          "mean": 0.0
        },
        "repair_regret_mean": 0.6842105263157895,
        "resolved": 119,
        "route_discovery": {
          "hi": 0.7226890756302521,
          "lo": 0.5462184873949579,
          "mean": 0.6386554621848739
        },
        "unsafe_total": 8
      }
    },
    "N": {
      "budget_outcomes": 144,
      "deepseek/deepseek-v4-flash": {
        "excess_escalation": {
          "hi": 0.05142083897158322,
          "lo": 0.02435723951285521,
          "mean": 0.036535859269282815
        },
        "f000_governance": {
          "hi": 0.23157894736842105,
          "lo": 0.12631578947368421,
          "mean": 0.17894736842105263
        },
        "f010_governance": {
          "hi": 0.1511627906976744,
          "lo": 0.06395348837209303,
          "mean": 0.10465116279069768
        },
        "finite_fallback_discovery": {
          "hi": 0.1511627906976744,
          "lo": 0.06395348837209303,
          "mean": 0.10465116279069768
        },
        "freeze_adaptation": {
          "hi": 0.7821380243572396,
          "lo": 0.7225981055480379,
          "mean": 0.7537212449255751
        },
        "governance_correct": {
          "hi": 0.13125845737483086,
          "lo": 0.08795669824086604,
          "mean": 0.10825439783491204
        },
        "optimal_route": {
          "hi": 0.10013531799729364,
          "lo": 0.06089309878213803,
          "mean": 0.07983761840324763
        },
        "repair_regret_mean": 2.003384094754653,
        "resolved": 739,
        "route_discovery": {
          "hi": 0.8267929634641408,
          "lo": 0.7699594046008119,
          "mean": 0.7997293640054127
        },
        "unsafe_total": 3
      },
      "episodes": 4860,
      "qwen/qwen3.7-flash": {
        "excess_escalation": {
          "hi": 0.06569343065693431,
          "lo": 0.041605839416058395,
          "mean": 0.052554744525547446
        },
        "f000_governance": {
          "hi": 0.42424242424242425,
          "lo": 0.3212121212121212,
          "mean": 0.3696969696969697
        },
        "f010_governance": {
          "hi": 0.16568047337278108,
          "lo": 0.09763313609467456,
          "mean": 0.1301775147928994
        },
        "finite_fallback_discovery": {
          "hi": 0.16568047337278108,
          "lo": 0.09763313609467456,
          "mean": 0.1301775147928994
        },
        "freeze_adaptation": {
          "hi": 0.6576642335766424,
          "lo": 0.6051094890510949,
          "mean": 0.6313868613138686
        },
        "governance_correct": {
          "hi": 0.21751824817518248,
          "lo": 0.1759124087591241,
          "mean": 0.19635036496350364
        },
        "optimal_route": {
          "hi": 0.061313868613138686,
          "lo": 0.03868613138686131,
          "mean": 0.049635036496350364
        },
        "repair_regret_mean": 0.3968253968253968,
        "resolved": 1370,
        "route_discovery": {
          "hi": 0.6693430656934306,
          "lo": 0.6175182481751825,
          "mean": 0.6437956204379562
        },
        "unsafe_total": 39
      },
      "transport_outcomes": 1761,
      "z-ai/glm-4.7-flash": {
        "excess_escalation": {
          "hi": 0.17612293144208038,
          "lo": 0.12647754137115838,
          "mean": 0.15011820330969267
        },
        "f000_governance": {
          "hi": 0.6331877729257642,
          "lo": 0.5065502183406113,
          "mean": 0.5676855895196506
        },
        "f010_governance": {
          "hi": 0.43258426966292135,
          "lo": 0.29775280898876405,
          "mean": 0.3651685393258427
        },
        "finite_fallback_discovery": {
          "hi": 0.43258426966292135,
          "lo": 0.29775280898876405,
          "mean": 0.3651685393258427
        },
        "freeze_adaptation": {
          "hi": 0.7458628841607565,
          "lo": 0.6867612293144209,
          "mean": 0.7163120567375887
        },
        "governance_correct": {
          "hi": 0.4562647754137116,
          "lo": 0.39243498817966904,
          "mean": 0.4243498817966903
        },
        "optimal_route": {
          "hi": 0.17612293144208038,
          "lo": 0.1288416075650118,
          "mean": 0.15130023640661938
        },
        "repair_regret_mean": 1.2935323383084578,
        "resolved": 846,
        "route_discovery": {
          "hi": 0.9645390070921985,
          "lo": 0.9361702127659575,
          "mean": 0.950354609929078
        },
        "unsafe_total": 118
      }
    }
  }
}
```
